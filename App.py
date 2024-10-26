from nutricionApp import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
#si falla simplemente quita esto "host='0.0.0.0', port=5200" o  port=5000