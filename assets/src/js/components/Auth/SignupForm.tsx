import { useForm } from "react-hook-form";
import useAuth from "./useAuth";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { useState } from 'react';

async function signupUser(credentials: any) {
  const url = "https://againstporn.org/api/accounts/signup/";
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

const SignupForm = () => {
  const { authData, 
          setLoading,
          signUp } = useAuth();
  const { register, handleSubmit } = useForm();
  const [error, setError] = useState('');
  const [failure, setFailure] = useState('');
  const onSubmit = async (data, e) => {
    e.preventDefault();
    setError('');
    setFailure('');
    if (!data?.password || !data?.password2) {
        setError('This field cannot be blank.')
    }
    else if (data?.password !== data?.password2) {
        setError("Passwords don't match.")
    }
    else {
      setError('');
      const response = await signupUser(data);
      if (response?.detail !== undefined) {
        setFailure(response.detail);
      }
      else if (typeof response?.email === 'object') {
        setFailure(response.email[0]);
      }
      else {
        setLoading(true);
        await signUp({ reports: '', email: data.email, token: '', verificationStatus: 'created'});
      }
    }
    return {error: error, failure: failure};
  } 
  return (
      <Form onSubmit={handleSubmit(onSubmit)}>
       <Form.Group className="mb-3 col-8 offset-2" controlId="formBasicEmail">
         <Form.Label>Email address</Form.Label>
          <Form.Control
            {...register("email")}
            type="email"
            placeholder="Email address"
            autoComplete="username"
          />
          <Form.Text className="text-center">We'll never share your email with anyone else.</Form.Text>
          {failure && 
             <>
              <Form.Control.Feedback type="invalid" className="d-flex justify-content-center">
               {failure}
              </Form.Control.Feedback>
             </>
           }
       </Form.Group>
       <Form.Group className="mb-3 col-8 offset-2" controlId="formBasicUsername">
        <Form.Label>Username (optional)</Form.Label>
        <Form.Control
          {...register("username")}
          type="text"
          placeholder="username"
          autoComplete="username"
        />
       </Form.Group>
       <Form.Group className="mb-3 col-8 offset-2" controlId="formBasicPassword1">
        <Form.Label>Password</Form.Label>
        <Form.Control
          {...register("password")}
          type="password"
          placeholder="Password"
          autoComplete="new-password"
        />
       </Form.Group>
       <Form.Group className="mb-3 col-8 offset-2" controlId="formBasicPassword2">
        <Form.Label>Confirm Password</Form.Label>
        <Form.Control
          {...register("password2")}
          type="password"
          placeholder="Password"
          autoComplete="new-password"
        />
          <Form.Text className="text-center">Enter the same password as before, for verification.</Form.Text>
          {error && 
             <>
              <Form.Control.Feedback type="invalid" className="d-flex justify-content-center">
               {error}
              </Form.Control.Feedback>
             </>
           }
       </Form.Group>
         <Button variant="success" className="col-4 offset-4 mt-2" type="submit">
          Sign up!
        </Button>
      </Form>
   );
};

export default SignupForm;
