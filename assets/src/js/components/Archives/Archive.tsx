import ScoreComments from './ScoreComments';
function Archive({ post }) {
    const {
        title,
        thumbnail,
        submitted,
        flair,
        nsfw,
        author,
        id
    } = post;
    var file = '/archives' + document.location.pathname + id + '/';
    var cond = flair !== null;
    return (
      <div className="row">
        <div className="thumbnail">
          <a href={id+'/'}>
            <img src={'/static/thumbnails/' + thumbnail} className={nsfw ? "nsfw" : ""} />
          </a>
        </div>
        <div id="body">
          <div id="title">
            <span>
              <a href={id+'/'}>{title}</a>
            </span>&nbsp;
            {cond && <span className="TNH">{flair}</span>}
          </div>
          <span id="date" className="text-muted">
            Submitted by {author} on {submitted}
          </span>&nbsp;
          <ScoreComments post={post} />
        </div>
      </div>
    )
}

export default Archive;
