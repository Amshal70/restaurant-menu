from flask import Flask, render_template, request, jsonify, send_file
from flask_mail import Mail, Message
import qrcode
from io import BytesIO
import sqlite3

app = Flask(__name__)

# Configuring Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Example using Gmail SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your_email_password'  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'  # Default sender email

mail = Mail(app)

# Sample Menu Data
menu_data = {
    "Pizza": ["Margherita", "Pepperoni", "Veggie"],
    "Burgers": ["Classic Burger", "Cheese Burger", "Vegan Burger"],
    "Broasts": ["Spicy Broast", "Mild Broast"],
    "Sandwiches": ["Chicken Sandwich", "Veg Sandwich"],
    "Pastas": ["Spaghetti", "Mac and Cheese"],
    "Wings": ["Buffalo Wings", "BBQ Wings"]
}

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY,
            rating INTEGER NOT NULL,
            comments TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Run database initialization before the first request
@app.before_request
def initialize():
    init_db()

# Save feedback to SQLite database
def save_feedback(rating, comments):
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('INSERT INTO feedback (rating, comments) VALUES (?, ?)', (rating, comments))
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html", menu=menu_data)

@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    feedback = request.get_json()
    rating = feedback.get('rating')
    comments = feedback.get('comments')

    # Save feedback to the database
    save_feedback(rating, comments)

    # Send feedback via email
    msg = Message("New Feedback from Customer", recipients=["restaurant_email@example.com"])
    msg.body = f"Rating: {rating}\nComments: {comments}"

    try:
        mail.send(msg)
        return jsonify({"message": "Thank you for your feedback!"})
    except Exception as e:
        return jsonify({"message": "Sorry, we couldn't submit your feedback at the moment. Please try again later."}), 500

# QR Code Generation Route
@app.route("/generate_qr")
def generate_qr():
    menu_url = "http://127.0.0.1:5000/"  # Local development URL, update for production deployment
    img = qrcode.make(menu_url)
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
