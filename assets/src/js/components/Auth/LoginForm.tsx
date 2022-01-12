import { useForm } from "react-hook-form";
import useAuth from "./useAuth";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { useState } from 'react';

async function loginUser(credentials: any): Promise<any> {
  const url = "https://againstporn.org/api/accounts/login/";
  const api_url =
    process.env.NODE_ENV === "production"
      ? url
      : url.replace("https://againstporn.org", "http://34.225.127.212:8000");
  return fetch(api_url,{
    method: 'POST',
    headers: {
     'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  })
   .then((data) => data.json())
   .catch((err) => console.log(err));
}

const LoginForm = () => {
  const { authData, 
          signIn,
          modeHandler: { setMode }
  } = useAuth();
  const { register, handleSubmit } = useForm();
  const [error, setError] = useState('');
  const onSubmit = async (data: any, e: any) => {
    e.preventDefault();
    const response = await loginUser(data);
    if (response.hasOwnProperty('token')) {
      const _email = data.email;
      signIn({ ...authData, token: response.token, email: _email, verificationStatus: `${JSON.stringify(response?.flair) || ""}`, reports: response?.reports });
    } else {
      setError(response?.detail || '');
    }
  };
  return (
    <Form onSubmit={handleSubmit(onSubmit)} className="col-8 d-flex flex-column offset-2">
      <Form.Group className="mb-3" controlId="formBasicEmail">
        <Form.Label>Email address</Form.Label>
        <Form.Control
          {...register("email")}
          type="email"
          placeholder="Email address"
          autoComplete="username"
        />
        {error && 
         <>
          <Form.Control.Feedback type="invalid" className="d-flex justify-content-center">
           {error}
          </Form.Control.Feedback>
         </>
         }
       </Form.Group>
       <Form.Group className="mb-3" controlId="formBasicPassword">
        <Form.Label>Password</Form.Label>
        <Form.Control
          {...register("password")}
          type="password"
          placeholder="Password"
          autoComplete="current-password"
        />
       </Form.Group>
       <Button variant="primary" className="offset-1 col-10 mt-3" type="submit">
         Submit
       </Button>
       <div className="text-center small mt-2">
         <button style={{ borderStyle: 'none',
                          backgroundColor: 'transparent', 
                          color: 'var(--blue)'
                       }}
                 onClick={() => setMode(3)}
         >
           Forgotten your username or password?
         </button>       
       </div>
     </Form>
   );
};

export default LoginForm;
