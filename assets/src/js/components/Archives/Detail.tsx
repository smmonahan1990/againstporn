import parse from 'html-react-parser';
import React from 'react';

export default function Detail(props) {
    const { post: { title,
                    author,
                    submitted,
                    flair,
                    nsfw,
                    fullsize,
                    selftext,
                    comments,
                    json
                  }, ...rest } = props; 
    const Report = React.lazy(() => import('./Report'));
//    const nsfw = typeof fullsize === 'string' && `${flair || ''}`.toLowerCase().match(/trigger warning/)
    const Pager = React.lazy(() => import('./Pager'));
    const Loading = React.lazy(() => import('../App/Loading'));
    return (
<>
<div id="post-body" className="mb-1">
  <div className="d-flex align-items-center">
   <React.Suspense fallback="">
    <Report />
   </React.Suspense>
   <h4 className="d-flex flex-grow-1 justify-content-end">
     {flair !== null && <span className="TNH mt-2 mr-1">{flair}</span>}
     <a href={document.location.pathname} className="font-weight-normal text-right" style={{ color: '#551A8B' }}>{title}</a>
   </h4>
 </div>
  {author !== undefined && submitted !== undefined && 
    <span className="font-weight-lighter mr-2" style={{ fontSize: '14px', marginTop: '5px' }}>
     Submitted by {author} to r/{document.location.pathname.split('/')[1]} on {submitted}
    </span>
  }
 <div id="post-content"> 
  <div className="dropdown-divider mb-3" style={{ borderTop: '1px solid black' }}></div>
  {document.readyState !== 'complete' && selftext === undefined && fullsize === undefined && 
   <React.Suspense fallback={<div className="d-flex flex-column text-center">Loading...</div>}>
    <Loading />
   </React.Suspense>
  }
  {selftext !== null && parse(selftext || '')}
  {fullsize !== null && fullsize !== undefined &&
   <>
    <div className="d-flex justify-content-center" style={{ paddingBlock: (nsfw ? '15px' : 'unset') }}>
     {nsfw && 
       <div id="nsfw" onClick={() => {
         $("#nsfw")[0].classList.toggle("d-none");
         $("img")[0].classList.remove("nsfw");
         }}
       >Click to Open NSFW
       </div>
     }
     <a href={"/static/" + fullsize}>
     <img className={nsfw ? "img-fluid nsfw" : "img-fluid"} style={{ maxHeight: '100vh', maxWidth: 'auto' }} src={"/static/"+fullsize}
      aria-label={title} />
     </a>
    </div>
   </>
  }
 <div className="dropdown-divider mt-3" style={{ borderTop: '1px solid black' }}></div>
 </div>
 <div className="d-flex justify-content-end small">
  <div style={{ wordBreak: 'break-all', whiteSpace: 'break-spaces' }} className="flex-fill text-monospace text-justify d-none flex-sm-shrink-1 flex-md-shrink-1 flex-lg-shrink-1" id="meta">{parse(json || '')}</div>
   <div className="flex-sm-shrink-3 flex-md-shrink-0 flex-lg-shrink-0 text-center font-italic">
  {comments || 0} comment{comments === 1 ? '' : 's'}
  &nbsp;&middot;&nbsp;
  <button id="showmeta" 
          onClick={() => {
             var x = $("#showmeta")[0].innerHTML;
             $('#meta')[0].classList.toggle('d-none');
             $("#showmeta")[0].innerHTML = x === 'see post metadata' ? 'hide post metadata' : 'see post metadata';
          }}
          style={{ border: 'none', backgroundColor: 'transparent', fontStyle: 'italic', marginLeft: '-5px', paddingTop: '0px' }}>
  see post metadata
  </button>
  </div>
 </div>
</div>
<React.Suspense fallback="">
 <Pager {...rest} />
</React.Suspense>
</>
)
}
