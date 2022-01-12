import Form from 'react-bootstrap/Form';
import { useFormContext } from 'react-hook-form';
import useAuth from './../Auth/useAuth';

export default function Flair() {
  const { authData } = useAuth();
  const items = authData?.verificationStatus?.flair_choices.map((a, b) => ([b+4, a[0]]));
  const { register } = useFormContext();
  return ( 
           <Form.Select 
              {...register('flair')}
              name="flair" 
              id="id_flair" 
              className="select form-control p-1 mb-3"
           >
            <option value="0">Select flair...</option>
             {items.map((item) =>
              <option key={item[0]} value={item[0]}>{item[1]}</option>
             )}
	   </Form.Select>
         )
}
