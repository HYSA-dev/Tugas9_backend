from app import create_app, db

app = create_app()

# Membuat tabel secara otomatis saat aplikasi pertama kali dijalankan
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)