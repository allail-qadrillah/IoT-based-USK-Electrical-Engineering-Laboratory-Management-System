from websites import create_app
import random

app = create_app()

if __name__ == '__main__':
  # app.run(debug=True, port=5000)
  # app.run(debug=False, port='0.0.0.0')
	app.run(host='0.0.0.0',  # Establishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)