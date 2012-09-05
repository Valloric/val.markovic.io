from fabric.api import lcd, local

import os
import hashlib

DEV_CONF = "site.yaml"
PROD_CONF = "site-prod.yaml"

def dev_regen():
  """Regenerate dev content"""
  local('rm -rf deploy')
  dev_gen()


def dev_gen():
  """Generate dev content"""
  local('hyde gen')


def serve():
  """Serve dev content"""
  local('hyde serve')


def prod_gen():
  """Build production content"""
  local("rm -rf prod_deploy/*")
  local( 'hyde gen -c {0}'.format( PROD_CONF ) )

  with lcd("prod_deploy"):
    for glob_path in [ 'media/js/*',
                       'media/less/*',
                       'media/img/*' ]:
      files = local( "echo {0}".format( glob_path ), capture=True ).split( " " )
      for filepath in files:
        file_hash = _hash_for_file( os.path.join( 'prod_deploy', filepath ) )
        print "[+] Hash for {0} is {1}".format( filepath, file_hash )

        newname = _get_new_filename( filepath, file_hash )
        local( 'mv {0} {1}'.format( filepath, newname ) )
        local( r"find . -type f -print0 | xargs -0 sed -i '' -e "
               '"'
               r"s:/{0}:/{1}:g"
               '"'.format( filepath, newname ) )

      # Fix permissions
      local( r"find * -type f -print0 | xargs -0 chmod a+r" )
      local( r"find * -type d -print0 | xargs -0 chmod a+rx" )


def prod_current():
  """Push to production, but use the current state of the 'deploy' folder."""
  # TODO: implement this
  pass


def prod_push():
  """Push to production. This first regenerates the site."""
  prod_gen()
  prod_current()


def _hash_for_file( filepath ):
  return hashlib.sha1( open( filepath, 'r' ).read() ).hexdigest()[ :8 ]


def _get_new_filename( filepath, file_hash ):
  # TODO: fix the problem with @2x images having a different hash prefix from
  # the non-@2x version
  path_without_extension, extension = os.path.splitext( filepath )
  at2x = ''
  if path_without_extension.endswith( '@2x' ):
    at2x = '@2x'
    path_without_extension = path_without_extension.replace( '@2x', '' )

  return "{0}.{1}{2}{3}".format( path_without_extension,
                                 file_hash,
                                 at2x,
                                 extension )

