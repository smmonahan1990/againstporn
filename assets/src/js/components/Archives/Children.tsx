import parse from 'html-react-parser';
import { useState } from 'react';

export default function Comment({ comment, i=0 }) {
  const { id, body, author, text, score, children, awards, date } = comment;
  const c = i === 0 ? 'post-comment w-100' : 'w-100';
  const d = i === 0 ? '' : 'post-comment-child nested-'+i;
  const deleted = (body === '<p>[deleted]</p>' || body === '<p>[removed]</p>') ? 'comment-deleted' : '';
  const replies = children.length > 1 ? children.length + ' replies' : children.length === 1 ? '1 reply' : '';
  function initState(n) {
    if (!(!n) && n % 5 === 0) {
        return ' d-none';
    } else {
        return '';
    }
  }
  const [show, setShow] = useState(initState(i)); 
  return (
   <>   
    {!(!show) &&
     <>
      <button onClick={() => setShow('')} 
              style={{ backgroundColor: 'transparent', 
                       borderStyle: 'none', 
                       color: '#0056b3'
              }}
      >
       Continue reading
      </button>
     </>
   }
   <div className={c + show}>
    <div className={d + (score < 1 ? " downvoted" : '')}>
     <div className={"comment-header "+deleted}>
      {deleted && 
       <>
        <i>(comment deleted or removed)</i>
        {replies && 
         <>
          &middot;
          <i>{replies}</i>
         </>
        }
        {children.length > 0 && 
          children.map((child, index) => <Comment key={index} comment={child} i={i+1} />)
        }
       </>
      }
      {!deleted && 
        <>
         <div className="w-100 d-flex justify-content-end">
          <button id="idarchives" className="blockquote-footer popover" onClick={() => document.getElementById(id).classList.toggle('d-none')}></button>
          <div className="comment-archive">
           {!(!awards) && parse(awards)}
           <span title={id}>{author}</span>
           {text !== null && 
            <span style={{ borderColor: 'var(--dark)', backgroundColor: 'var(--dark)',color: 'white' }} className="user-flair">{text}</span>
           }
            &middot;
           <span>{score}</span>
            &middot;
           <span>{date}</span>
           {replies && 
            <>
             &middot;
             <span className="text-muted">{replies}</span>
            </>
            }
          </div>
         </div> 
        </>
       }
      </div>
      {!deleted && 
       <>
        <div id={id} className={"comment-body" + (score < 1 ? " d-none" : '')}>
         <div>{parse(body)}</div>
          {children.length > 0 && 
            children.map((child, index) => <Comment key={index} comment={child} i={i+1} />
          )}
        </div>
       </>
      }
   </div>
  </div>
  </>
  )
}

