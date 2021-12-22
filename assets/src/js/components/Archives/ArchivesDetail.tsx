import React, { Component } from "react";
import Detail from './Detail';
import ArchivesService from './ArchivesService';
import { ComponentProps, ArchiveItem } from './ArchivesList';
import Comment from './Children';
import Pager from './Pager';

const service = new ArchivesService();
interface CommentItem {
    author: string;
    body: string;
    date: string;
    id: string;
    score: number;
    text: string;
    children: Array<CommentItem>;
}

interface ComponentState {
    post: ArchiveItem | string;
    comments: Array<CommentItem>;
    next: string;
    previous: string;
}

class ArchivesDetail extends Component<ComponentProps, ComponentState> {
    constructor(props: ComponentProps) {
        super(props);
        this.state = {
            post: '',
            comments: [],
            next: '',
            previous: '',
        }
    }
    componentDidMount() {
        service.getArchivesByURL(document.location.pathname.slice(1)).then((result) => {
            this.setState({
                post: result.post,
                comments: result.comments,
                next: result.next,
                previous: result.prev
            })
        })
        .catch((err) => console.log(err));
    }       
    shouldComponentUpdate() {
        return true;
    }
    render() {
        const Pager = React.lazy(() => import('./Pager'));
        const { comments, ...props } = this.state;
        return (
          <div className="container d-flex flex-column">
            {this.shouldComponentUpdate() &&
             <>
              <Detail {...props} />
              <div className={"flex-grow-1" + (comments.length === 1 ? ' d-flex' : '')}>
               {comments.length > 0 && 
                 <>
                  <div className={"mt-2 mb-2 flex-fill" + (comments.length === 1 ? ' d-flex align-items-end' : '')}>  
                   {comments.map((comment, index) =>
                    <Comment key={index} comment={comment} />
                   )}
                  </div>
                 </>
               }
               {comments.length > 1 &&
                <React.Suspense fallback={<div className="text-center">Loading...</div>}>
                 <Pager {...props} />
                </React.Suspense>
               }
              </div>
             </>
            }
          </div>
        )
    }
}

export default ArchivesDetail;
