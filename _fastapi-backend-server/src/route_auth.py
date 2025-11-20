from fastapi import Request, HTTPException, APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse

auth_router = APIRouter()

@auth_router.get("/verify-backend-access")
def verify_backend_access(request: Request):
    user = request.cookies.get("session_token")
    if user == "backend_user_token":
        return {"access": "granted"}
    raise HTTPException(status_code=401, detail="Not authorized")

@auth_router.get("/login")
def display_login_page():
    """Display login page (route_auth)"""
    html = """
    <html>
        <body>
            <h2>Accès Backend</h2>
            <form action="/api-backend/login" method="post">
                <input type="password" name="password" placeholder="Mot de passe" required>
                <button type="submit">Se connecter</button>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html)

# Give access to env variables
import os
from dotenv import load_dotenv
load_dotenv()
@auth_router.post("/login")
def submit_login(password: str = Form(...)):
    """Process form submit  (route_auth)"""
    basic_pwd_auth = os.getenv('BASIC_PWD_AUTH')
    # Get password from .env
    basic_pwd_auth = os.getenv('BASIC_PWD_AUTH')  # Basic password authentication
    if password == basic_pwd_auth:  # BASIC STUPID AUTHENTIFICATION
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie("session_token", "backend_user_token", path="/")
        return response
    else:
        return HTMLResponse("Invalid password", status_code=401)

@auth_router.get("/logout")
def logout():
    """ Delete authentification session cookie (route_auth)"""
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="session_token", path="/")
    return response