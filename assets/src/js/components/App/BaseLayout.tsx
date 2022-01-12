import { Route, Switch } from "react-router-dom";
import { Suspense, lazy } from 'react';
import Modal from './Modal';

const AuthForm = lazy(() => import("../Auth/AuthForm"));
const ArchivesList = lazy(() => import("../Archives/ArchivesList"));
const ArchivesDetail = lazy(() => import("../Archives/ArchivesDetail"));

function NavLink(props: {label: string}): JSX.Element {
  const p = document.location.pathname.split('/',2).reduceRight((item) => item);
  const path = '/' + props.label.toLowerCase() + '/';
  const q = p === path.slice(1,-1) ? 'nav-link active' : 'nav-link';

  return (
    <li className="nav-item">
      <a className={q} href={path}>
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
         <NavLink label="AntiKink" />
         <NavLink label="AntiPornography" />
         <NavLink label="PornFree" />
         <NavLink label="PornFreeWomen" />
         <NavLink label="PornHatesWomen" />
         <NavLink label="PornIsMisogyny" />
         
        </ul>
        <Suspense fallback={<div className="d-flex align-items-center">Loading...</div>}>
        <AuthForm />
        </Suspense>
      </div>
    </nav>
    <div className="content d-flex flex-grow-1 mt-4">
     <Suspense fallback={<div>Loading...</div>}>
      <Switch>
       
       <Route path="/antikink/" exact component={ArchivesList} />
       <Route path="/antipornography/" exact component={ArchivesList} />
       <Route path="/pornfree/" exact component={ArchivesList} />
       <Route path="/pornfreewomen/" exact component={ArchivesList} />
       <Route path="/pornhateswomen/" exact component={ArchivesList} />
       <Route path="/pornismisogyny/" exact component={ArchivesList} />
       <Route path="/antikink/:id/" component={ArchivesDetail} />
       <Route path="/antipornography/:id/" component={ArchivesDetail} />
       <Route path="/pornfree/:id/" component={ArchivesDetail} />
       <Route path="/pornfreewomen/:id/" component={ArchivesDetail} />
       <Route path="/pornhateswomen/:id/" component={ArchivesDetail} />
       <Route path="/pornismisogyny/:id/" component={ArchivesDetail} />
      </Switch>
    </Suspense>
    </div>
    <div className="footer">
      <NavLink label="AntiKink" />
      <NavLink label="AntiPornography" />
      <NavLink label="PornFree" />
      <NavLink label="PornFreeWomen" />
      <NavLink label="PornHatesWomen" />
      <NavLink label="PornIsMisogyny" />
    </div>
    <Modal />
  </div>
);

export default BaseLayout;
