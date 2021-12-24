import useAuth from "./useAuth";

export default function AppStack() {
  const { authData, 
          signOut, 
          modeHandler: { setMode }
        } = useAuth();
  const authString = !authData ? 'new user' : authData?.email;
  return (
    <ul className="navbar-nav ml-auto">
      <li className="nav-item">
        <button
          className="nav-link dropdown-toggle"
          id="navbarDropdown"
          role="button"
          data-toggle="dropdown"
          aria-haspopup="true"
          aria-expanded="false"
        >
          Hi, {authString.split('@')[0]}!
        </button>
        <div
          className="dropdown-menu ml-1 dropdown-menu-lg-right"
          aria-labelledby="navbarDropdown"
        >
          <button className="dropdown-item">
            Create a new post
          </button>
          <div className="dropdown-divider"></div>
          <button className="dropdown-item" onClick={() => setMode(8)}>
            Change password
          </button>
          <div className="dropdown-divider"></div>
          <button className="dropdown-item" onClick={signOut}>
            Log Out
          </button>
        </div>
      </li>
    </ul>
  );
}
