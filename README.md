# 📚 Book Trader – Rent & Sell Books Online

**Book Trader** is a web platform designed to facilitate the buying, selling, and renting of used books while building a community of book lovers. Users can list their books, browse or search listings, and connect with others — promoting both sustainability and a love for reading.

---

## 🌟 Features

- **User Registration & Login**  
  Secure account creation and authentication system.

- **Book Listings**  
  Users can upload books they want to rent or sell, specifying title, genre, price, and rent duration.

- **Advanced Book Search**  
  Search books by title, author, price range, seller, or rent duration.

- **Transactions**  
  Rent or buy books with a seamless transaction flow. Track purchases and rentals.

- **Returns**  
  Renters can return books, automatically re-listing them on the site.

- **User Profiles**  
  View all personal listings, transaction history, and friends.

- **Social Features**  
  Follow friends and explore book listings from people nearby or within your social circle.

---

## 🛠 Tech Stack

- **Frontend**: Vue.js  
- **Backend**: Flask (Python)  
- **Database**: SQLite  

---

## 🚀 Getting Started

Follow this step-by-step guide to run the project locally:

### 1. Clone the repository

```bash
git clone https://github.com/YangZhou17/Book-Trader.git
cd Book-Trader/
```

### 2. Set up the frontend

```bash
sudo apt update
sudo apt install nodejs npm -y
node -v         # verify Node.js installation
npm -v          # verify npm installation

npm install -g yarn
yarn -v         # verify Yarn installation

yarn global add @vue/cli
vue --version   # verify Vue CLI installation

yarn install
yarn run serve  # frontend runs on http://localhost:8080
```

### 3. Set up the backend

```bash
sudo apt install python3 -y  # if not installed

cd backend/
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
flask run --port=5001  # backend runs on http://localhost:5001
```

> ✅ After both frontend and backend are running, open your browser and go to **[http://localhost:8080](http://localhost:8080)** to access the Book Trader web app.

---

### 🔁 Running the Project Again (After First Setup)

Once you’ve completed the initial setup, you can start the project anytime with just these commands:

**Frontend:**
```bash
yarn run serve
```

**Backend:**
```bash
cd backend/
source venv/bin/activate
flask run --port=5001
```

---

### 🛑 Terminate the App

To stop the servers:

- Press `Ctrl+C` in both frontend and backend terminal windows  
- Run `deactivate` in the backend terminal to exit the virtual environment

---

### ⚠️ Troubleshooting

If you encounter setup issues, please try using the following versions for compatibility:

```bash
node -v        # v18.19.1
npm -v         # 9.2.0
yarn -v        # 1.22.22
vue --version  # @vue/cli 5.0.8
python3 -V     # Python 3.12.3
```

You can use tools like [`nvm`](https://github.com/nvm-sh/nvm) and [`pyenv`](https://github.com/pyenv/pyenv) to manage different versions easily.

---

## 👥 Authors & Contributors

*(Sorted alphabetically by first name)*

- Elaine Xing  
- Helen Sun  
- Jasper Wang  
- Vicky Yang  
- Yang Zhou

---

## 💡 Future Enhancements

- Real-time messaging between users
- Book recommendation engine
- User reviews and ratings
- Buy/Rent request system (owner can approve/decline offers)
