function Pager({ previous, next }) {
 return (
 <>
 <div className="d-flex align-items-center mb-1 small">
  <div className="align-items-center d-flex flex-grow-1 flex-row-reverse mr-1" style={{ flexBasis: '50px' }}>
   <a className="order-1" href={previous}>
    <i style={{ color: "#551A8B" }} className="fa fa-arrow-square-left"></i>
   </a>
   <span className="ml-1">Previous</span>
  </div>
  <div className="align-items-center flex-grow-1 d-flex ml-1" style={{ flexBasis: '50px' }}>
   <a className="order-1" href={next}>
    <i style={{ color: "#551A8B" }} className="fa fa-arrow-square-right"></i>
   </a>
   <span className="mr-1">Next</span>
  </div>
 </div>
 </>
 )
}

export default Pager;
