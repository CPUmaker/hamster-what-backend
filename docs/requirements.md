# Requiements

## 1. Introduction

The Budget Saver app is a mobile application designed to help users track their expenses and save money. The app includes features such as bill recording, login/register, profile management, expense tracking by category, statistics and trend charts, and a display of discount and coupons. The purpose of this document is to define the requirements for the Budget Saver app.

## 2. Functional Requirements

### 2.1 Bill Recording

The app should allow users to record bills and expenses by entering the following information:

- Bill name
- Bill category
- Bill amount
- Bank Account
- Due date

The app should also provide the option to set reminders for upcoming bills.

### 2.2 Login/Register

The app should allow users to create an account or log in with existing accounts. The login/register feature should support the following authentication methods:

- Email, username and password
- Social accounts (e.g. Google, Apple, Facebook)

### 2.3 Profile Management

The app should allow users to view and update their profiles. The profile should include the following information:

- Name
- Username
- Email address
- Password (can be changed)
- Bio
- Country
- City
- Birthday
- Affiliation
- Profile picture

### 2.4 Expense Tracking by Category

The app should allow users to categorize their expenses and view a list of expenses by category. The categories should include, but not limited to:

- Food
- Groceries
- Transportation
- clothing
- Entertainment
- Bill
- Sports
- Electronics
- Travel
- House & Car
- Others

The app should also allow users to add new categories and edit existing ones.

### 2.5 Statistics and Trend Charts

The app should provide users with statistics and trend charts to help them analyze their spending habits. The statistics and charts should include, but not limited to:

- Total expenses and income
- Expenses and income by category
- Monthly expenses and income trend

### 2.6 Display of Discounts and Coupons

The app should display discounts and coupons from various sources such as local stores and online retailers. The app should allow users to filter and search for discounts and coupons based on category and location.

## 3. Non-Functional Requirements

### 3.1 Performance

The app should be able to handle a large amount of data without performance issues. The app should also load quickly and respond to user actions in a timely manner.

### 3.2 Security

The app should ensure the security of user data and use encryption to protect user data in transit and at rest followed by items below:

- HTTPS should be implemented to ensure secure communication between the user's device and the server. This will help prevent man-in-the-middle attacks and eavesdropping.

- Tokens should be used for user authentication, which helps prevent attacks such as session hijacking and cross-site request forgery (CSRF).

- Passwords should be hashed using a strong hashing algorithm before storing them in the database. This ensures that even if the database is compromised, passwords cannot be easily retrieved.

- The app should use a salt when hashing passwords to further enhance security.

- Passwords should be checked against commonly used passwords and known compromised passwords to ensure that users are not using weak passwords.

The app should also follow industry-standard security practices to prevent unauthorized access to user accounts.

### 3.3 User Experience

The app should provide a user-friendly and intuitive interface. The app should also be accessible to users with disabilities.

### 3.4 Platform Compatibility

The app should be compatible with the latest versions of popular mobile platforms such as Android and iOS.

## 4. Constraints

The development of the Budget Saver app should adhere to the following constraints:

- The app should be developed using modern software engineering practices and follow coding standards.
- The app should be developed using scalable and maintainable architecture.
- The app should be developed within a reasonable budget and timeframe.
- The app should be tested thoroughly to ensure quality and reliability.
