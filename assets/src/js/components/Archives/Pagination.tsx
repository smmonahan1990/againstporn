import Pagination from 'react-bootstrap/Pagination';

function PageXofY(props) {
   const { state: { 
             archives,
             nextPageURL: x,
             prevPageURL: y,
             numPages: z 
         } } = props;
   const a = x === 1 ? (z - y === 1 ? z : 1) : x - 1;
   return (
      <p>
         {isNaN(parseInt(x)) || isNaN(parseInt(y))
           ? 'Loading...' 
           : archives.length === 0 
           ? 'No results found.' 
           : 'Page ' + a + ' of ' + z + '.'
         }
      </p>
   )
}

function MyPagination(props) {
  const { getPage, 
          state : { 
            nextPageURL: next,
            prevPageURL: prev, 
            numPages: total
        } } = props;

  if (isNaN(next) || isNaN(prev) || total === 1)
    return <br />

  function func(n) {
    const page = document.location.pathname.slice(1)+"?page="+n;
    return () => getPage(page);
  }      
  const PageItem = ({ n }) =>
    <Pagination.Item onClick={func(n)}>{n}</Pagination.Item>

  const current = (prev <= 2 && 2 < next) ? (next + prev) / 2 : next === 2 ? 1 : total === 1 ? 1 : prev + 1;
  let f1, b1, f2, b2;

  if (total > 6) {
      f1 = next;
      f2 = next === total ? 1 : next + 1;
      b1 = prev;
      b2 = prev - 1 === 0 ? total : prev - 1;
  }    

  return (
   <Pagination className="justify-content-center">
    <Pagination.First onClick={func(1)}/>
    <Pagination.Prev onClick={func(prev)}/>
    {b2 && <PageItem n={b2} />}
    {b1 && <PageItem n={b1} />}
    <Pagination.Item active>{current}</Pagination.Item>
    {f1 && <PageItem n={f1} />}
    {f2 && <PageItem n={f2} />}
    <Pagination.Next onClick={func(next)}/>
    <Pagination.Last onClick={func(total)}/>
   </Pagination>
  )
}

export { PageXofY, MyPagination };
