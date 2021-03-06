from fabric.api import lcd, local, prefix

from os import path
import hashlib
import platform

DEV_CONF = 'site.yaml'
PROD_CONF = 'site-prod.yaml'

# Mac sed and Linux sed don't have a compatible way of saying "modify in-place
# without a backup" so we have to do it in two different ways.
# See here for details: http://stackoverflow.com/q/5694228/1672783
SED_INPLACE_ARG = '-i' if platform.system() != 'Darwin' else "-i ''"

def dev_regen():
  """Regenerate dev content"""
  local( 'rm -rf deploy' )
  dev_gen()


def dev_gen():
  """Generate dev content"""
  local( 'hyde gen' )


def serve():
  """Serve dev content"""
  # By default, hyde serves from localhost instead of 0.0.0.0. This means that
  # we can't access it from other devices. With 0.0.0.0 we can.
  local( 'hyde serve -a 0.0.0.0' )


def prod_gen():
  """Build production content"""
  local( 'rm -rf prod_deploy/*' )
  local( 'hyde gen -c {0}'.format( PROD_CONF ) )

  # We need to unset LANG and set LC_CTYPE=C for Mac OS X Mountain Lion; see
  # here for more details: https://github.com/Homebrew/homebrew-dupes/pull/21
  # If we don't do this, we'll get "sed: RE error: illegal byte sequence"
  with prefix( 'unset LANG && export LC_CTYPE="C"' ):
    with lcd( 'prod_deploy' ):
      hash_store = {}
      for glob_path in [ 'media/js/*',
                        'media/less/*',
                        'media/img/*' ]:
        files = local( 'echo {0}'.format( glob_path ), capture=True ).split( ' ' )
        for filepath in files:
          file_hash = _hash_for_file( path.join( 'prod_deploy', filepath ) )
          hash_store[ filepath ] = file_hash
          print '[+] Hash for {0} is {1}'.format( filepath, file_hash )

          new_path = _get_new_filepath( filepath, file_hash, hash_store )
          local( 'mv {0} {1}'.format( filepath, new_path ) )
          local( r"find . -type f -print0 | xargs -0 sed {2} -e "
                '"'
                r's:/{0}:/{1}:g'
                '"'.format( filepath, new_path, SED_INPLACE_ARG ) )

        # Fix permissions
        local( r'find * -type f -print0 | xargs -0 chmod a+r' )
        local( r'find * -type d -print0 | xargs -0 chmod a+rx' )
        # fucking .DS_Store...
        local( 'find . -name ".DS_Store" -print0 | xargs -0 rm -rf' )


def _s3cmd_operation( operation,
                      path,
                      dest_path=None,
                      extra_options=[],
                      force_mime=None ):
  options = ' '.join( extra_options )
  if dest_path is None:
    dest_path = path.replace( 'prod_deploy/', '' )

  mime_arg = ''
  if force_mime is None:
    guess_mime_arg = '--guess-mime-type'
  else:
    guess_mime_arg = ''
    mime_arg = "--mime-type='{0}'"
    if force_mime:
      mime_arg = mime_arg.format( force_mime )
    else:
      # when force_mime is an empty string, don't add any mime
      mime_arg = ''

  local( 's3cmd '
         '{guess_mime} '
         '{mime_arg} '
         '--config=/vagrant/.s3cfg '
         # We must not let s3cmd use libmagic for --guess-mime-type because it's
         # shit; it guesses text/plain for .css and .js. The fallback works
         # better.
         '--no-mime-magic '
         '--acl-public '
         '{options} '
         '{operation} '
         '{path} '
         's3://val.markovic.io/{dest_path}'.format(
           options=options,
           operation=operation,
           path=path,
           dest_path=dest_path,
           mime_arg=mime_arg,
           guess_mime=guess_mime_arg ) )


def _s3cmd_sync( path, dest_path=None, extra_options=[], force_mime=None ):
  _s3cmd_operation( 'sync', path, dest_path, extra_options, force_mime )


def prod_current():
  """Push to production, but use the current state of the 'prod_deploy'
  folder."""

  # no --delete-remove!
  _s3cmd_sync( 'prod_deploy/',
               extra_options=[
                 "--exclude='favicon*'",
                 "--exclude='media/*'",
                 "--exclude='articles/*'",
                 # max-age is one hour
                 "--add-header='Cache-Control:public;max-age=3600'" ],
               force_mime='text/html; charset=utf-8' )

  _s3cmd_operation( 'put',
                    'prod_deploy/articles/atom.xml',
                    force_mime="application/atom+xml" )

  _s3cmd_sync( 'prod_deploy/articles/',
               extra_options=[
                 '--delete-removed',
                 # max-age is one hour
                 "--add-header='Cache-Control:public;max-age=3600'" ],
               force_mime='text/html; charset=utf-8' )

  _s3cmd_sync( 'prod_deploy/favicon*',
               dest_path='',
               extra_options=[
                 # max-age is one week
                 "--add-header='Cache-Control:public;max-age=604800'" ] )

  _s3cmd_sync( 'prod_deploy/media/',
               extra_options=[
                 '--delete-removed',
                 # max-age is one year, the RFC maximum
                 "--add-header='Cache-Control:public;max-age=31536000'" ] )

def prod_push():
  """Push to production. This first regenerates the site."""
  prod_gen()
  prod_current()


def _hash_for_file( filepath ):
  return hashlib.sha1( open( filepath, 'r' ).read() ).hexdigest()[ :8 ]


def _get_new_filepath( filepath, file_hash, hash_store ):
  """Computes the new filepath for the give path. The new path has the hash of
  the file inserted before the file extension, eg. foo.jpg -> foo.12345678.jpg

  There's a small complication because of images that use the @2x suffix; those
  images have to have the same prefix as the smaller images wiouth the '@2x'.
  For instance, retina.js will replace all references to foo.jpg with foo@2x.jpg
  on HiDPI screens. This means that something like foo.12345678.jpg will be
  replaced with foo.12345678@2x.jpg, so the bigger image needs to use the hash
  of the smaller version.

  This is not a problem because the visual content of the smaller and the @2x
  versions of the image will always be in sync even if the byte-wise content is
  not. So the @2x version will change only when the smaller one changes as
  well."""

  path_without_extension, extension = path.splitext( filepath )
  at2x = ''
  hash_to_use = file_hash
  if path_without_extension.endswith( '@2x' ):
    at2x = '@2x'
    path_without_extension = path_without_extension.replace( '@2x', '' )
    hash_to_use = hash_store[ filepath.replace( '@2x', '' ) ]

  return '{0}.{1}{2}{3}'.format( path_without_extension,
                                 hash_to_use,
                                 at2x,
                                 extension )

