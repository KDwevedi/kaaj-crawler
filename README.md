# Project README

## Instructions to Run

1. **Clone the Repository**  
   Clone this repository to your local machine.

2. **Ensure Required Ports are Available**  
   Make sure the following ports are not in use:
   - **Frontend:** `3000`
   - **Backend:** `5001`
   - **Database:** `5432`

3. **Run the Application**  
   Use the following command to build and start the application:
   ```bash
   docker compose up -d --build
   ```

4. **Access the Services**  
   - **Frontend (FE):** Accessible at `http://localhost:3000`
   - **Backend (BE):** Accessible at `http://localhost:5001`
   - **Database (DB):** Running on port `5432`

---

## Demo Video

https://github.com/user-attachments/assets/c31a0cfe-1627-456c-8643-638f59e32656



---

## Possible Improvements

1. **Playwright Parser Enhancement**  
   - The Playwright parser currently does not retrieve all details for businesses.

2. **Code Cleanup**  
   - Some hardcoded values for API calls can be replaced with environment configurations for better maintainability and flexibility.
