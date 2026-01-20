# E-commerce API

## Overview

This is a RESTful API for an e-commerce platform.

## Installation

To get started, clone this repository and install the dependencies:

```bash
git clone https://github.com/madihanazir/ecommerce-api.git
cd ecommerce-api
npm install
```

## Usage

### Endpoints

- `POST /register`
- `POST /login`
- `POST /forgot-password`
- `POST /reset-password`

## Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant AuthService
    participant EmailService

    User->>AuthService: Register
    AuthService-->>EmailService: Send verification email
    EmailService-->>User: Verification email
    User->>AuthService: Verify email
    AuthService->>User: Email verified
    User->>AuthService: Login
    AuthService->>User: Auth Token
    User->>AuthService: Forgot Password
    AuthService-->>EmailService: Send reset email
    EmailService-->>User: Reset password email
    User->>AuthService: Reset Password
    AuthService->>User: Password reset successful
```  

## License

This project is licensed under the MIT License.