import { Route, Switch } from "react-router-dom";
import { Suspense, lazy } from 'react';
import Modal from './Modal';

const AuthForm = lazy(() => import("../Auth/AuthForm"));
const ArchivesList = lazy(() => import("../Archives/ArchivesList"));
const ArchivesDetail = lazy(() => import("../Archives/ArchivesDetail"));

function NavLink(props: {path: string; label: string}): JSX.Element {
  const p = document.location.pathname.split('/')[1];
  const q = p === props.path.split('/')[1] ? "nav-link active" : "nav-link";
  return (
    <li className="nav-item">
      <a className={q} href={props.path}>
        {props.label}
      </a>
    </li>
  )
}

const BaseLayout = () => (
  <div className="d-flex flex-column flex-fill">
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark d-flex">
      <a className="navbar-brand" href="/antikink/">
        Home
      </a>
      <button
        className="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarNavAltMarkup"
        aria-controls="navbarNavAltMarkup"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span className="navbar-toggler-icon"></span>
      </button>
      <div className="flex-grow-1 collapse navbar-collapse" id="navbarNavAltMarkup">
        <ul className="navbar-nav mr-auto">
          <NavLink path="/antikink/" label="AntiKink" />
          <NavLink path="/antipornography/" label="AntiPornography" />
        </ul>
        <Suspense fallback={<div className="d-flex justify-content-center">Loading...</div>}>
        <AuthForm />
        </Suspense>
      </div>
    </nav>
    <div className="content d-flex flex-grow-1 mt-4">
     <Suspense fallback={<div>Loading...</div>}>
      <Switch>
       <Route path="/antikink/" exact component={ArchivesList} />
       <Route path="/antipornography/" exact component={ArchivesList} />
       <Route path="/antikink/:id/" component={ArchivesDetail} />
       <Route path="/antipornography/:id/" component={ArchivesDetail} />
      </Switch>
    </Suspense>
    </div>
    <div className="footer">
      <NavLink path="/antikink/" label="AntiKink" />
      <NavLink path="/antipornography/" label="AntiPornography" />
    </div>
    <Modal />
  </div>
);

export default BaseLayout;
