import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import Button from 'react-bootstrap/Button';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import AsyncLocalStorage from '@react-native-async-storage/async-storage';

async function reportArchive(data: any) {
  
  var url = 'https://againstporn.org/api'+document.location.pathname;
  url = process.env.NODE_ENV === 'production'
        ? url 
        : 'http://34.225.127.212:8000/api'+document.location.pathname;
//  const auth = await AsyncLocalStorage.getItem('@AuthData');
//  const token = JSON.parse(auth).token;
//  const headers = new Headers();
//  headers.set('Authorization','Token ' + token);
//  headers.set('Content-Type','application/json'); 
  return fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then((data) => data.json())
  .catch((err) => console.log(err));
}
  
function FormExample() {
//  const [validated, setValidated] = useState(false);
  const { register, handleSubmit } = useForm();
  const onSubmit = async (data, event) => {
//   const form = event.currentTarget;
    console.log(data);
//    if (form.checkValidity() === false) {
      event.preventDefault();
//      event.stopPropagation();
      const response = await reportArchive(data);
//    }

//    setValidated(true);
  };

  return (
   <Form onSubmit={handleSubmit(onSubmit)}>
    <Row className="mb-3">
     <Form.Group as={Col} className="offset-3 col-6" controlId="formGridModerate">
      <Form.Label className="mr-2">Moderate:</Form.Label>
      <Form.Select {...register('mod_action')}
        defaultValue="Choose moderation action..."
      > 
        <option>Choose moderation action...</option>
        <option>mark nsfw</option>
        <option>delete</option>
      </Form.Select>
     </Form.Group>
    </Row>
    <Button className="offset-4 col-4" variant="danger" type="submit">Submit form</Button>
   </Form>
  );
}

export default FormExample;
