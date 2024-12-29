envsubst '$DOMAIN $SSL_CERT_FILE_NAME $SSL_CERT_KEY_FILE_NAME' <"/etc/nginx/conf.d/$1" >/etc/nginx/conf.d/app.conf

while true; do
	# Use curl to send a request and capture the HTTP status code
	# NOTE: default port of api_server is 5000
	status_code=$(curl -o /dev/null -s -w "%{http_code}\n" "http://api-server:5000/health")

	# Check if the status code is 200
	if [ "$status_code" -eq 200 ]; then
		echo "API server responded with 200, starting nginx..."
		break # Exit the loop
	else
		echo "API server responded with $status_code, retrying in 5 seconds..."
		sleep 5 # Sleep for 5 seconds before retrying
	fi
done

# Start nginx and reload every 6 hours
while :; do
	sleep 6h &
	wait
	nginx -s reload
done &
nginx -g "daemon off;"
