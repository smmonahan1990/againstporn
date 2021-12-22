function ScoreComments(props) {
    const { score, comments } = props.post;
    var s = score === null ? 1 : score;
    var c = comments === null ? 0 : comments;
    var substr1 = (parseInt(s) === 1 ? 'point' : 'points')
    var substr2 = (parseInt(c) === 1 ? 'comment' : 'comments')
    var ps = (parseInt(s) < 1000 ? s : s[0] + ',' + s.slice(1,4))
    var pc = (parseInt(c) >= 200 ? '200+' : c)
    var result = ps + ' ' + substr1 + ' | ' + pc + ' ' + substr2;
    return <span className="comments-score">{result}</span>;
}

export default ScoreComments;
