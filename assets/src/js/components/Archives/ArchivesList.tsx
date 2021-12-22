import React, { Component } from 'react';
import Form from './Form';
import Archive from './Archive';
import ArchivesService from './ArchivesService';
import { PageXofY, MyPagination } from './Pagination';
const archivesService = new ArchivesService();

interface ComponentProps {
    default: any;
}

interface ArchiveItem {
    id: string;
    title: string;
    submitted: string;
    author: string;
    selftext: string;
    flair: string;
    comments: string;
    score: string;
    fullsize: string;
    json: string;
}

interface ComponentState {
    archives: Array<ArchiveItem>;
    numPages: number | string;
    nextPageURL: number | string;
    prevPageURL: number | string;
    flair: [string, string];
}

class ArchivesList extends Component<ComponentProps, ComponentState> {
    constructor(props: ComponentProps) {
        super(props);
        this.state = {
            archives: [],
            numPages: 1,
            nextPageURL: '',
            prevPageURL: '',
            flair: ['',''],
        };
    }
    componentDidMount() {
        archivesService.getArchives(document.location.pathname, document.location.search).then((result) => {
            this.setState({
                archives: result.data,
                numPages: result.numpages,
                nextPageURL: result.nextlink,
                prevPageURL: result.prevlink,
                flair: result.flair,
            })
        })
        .catch((err) => console.log(err));
    }

    shouldComponentUpdate() {
        return true;
    }

    getPage = (params) => {
        archivesService.getArchivesByURL(params).then((result) => {
            this.setState({
                archives: result.data,
                nextPageURL: result.nextlink,
                prevPageURL: result.prevlink
            })
        });
    };

    render() {
      const { ...props } = this;
      return (
        <div className="container">
          <Form t={this} />
          <br />
          {this.shouldComponentUpdate() && 
            <>
             <PageXofY {...props} />
             {this.state.archives.map((a) =>
               <Archive post={a} key={a.id} />
             )}
              <MyPagination {...props} />
            </>
          }
        </div>
       )
    }
}

export default ArchivesList;
export { ComponentProps, ArchiveItem };
