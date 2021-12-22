import React from 'react';
import CustomModal from '../App/Modal';
import useAuth from '../Auth/useAuth';

interface Fancy {
  value: number;
  inner: string;
  css: string;
  ref: React.ForwardedRef<any>;
}

export default function AuthStack(): JSX.Element {
  const { modeHandler : { setMode } } = useAuth();
  const FancyButton: React.ForwardRefExoticComponent<Fancy> = React.forwardRef((props, ref) => {
    const { value, inner, css } = props;
    return (
     <button ref={ref}
             className={css}
             onClick={() => setMode(value)}
     >
      {inner}
     </button>
    )
  });
  const ref1 = React.createRef();
  const ref2 = React.createRef();
  return (
   <>
    <form className="form-inline ml-auto">
     <FancyButton css="btn btn-outline-secondary" value={1} inner="Log in" ref={ref1} />
     <FancyButton css="btn btn-primary ml-2" value={2} inner="Sign Up" ref={ref2} />
    </form>
     <CustomModal />
   </>
  )
}
  
