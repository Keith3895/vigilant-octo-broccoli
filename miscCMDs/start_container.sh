docker run -d --name identity-service\
 -p 4000:80 -e APP_MODULE="identity_server:create_app()"\
 -e AUTHLIB_INSECURE_TRANSPORT="true"\
  -v /Users/keithfranklin/Documents/Exploring\ Programming/identity-service/instance:/app/instance myimage