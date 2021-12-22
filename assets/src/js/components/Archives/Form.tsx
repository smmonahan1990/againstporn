function Choices(props) {
    return <option value={props.inner}>{props.outer}</option>;
}
function Select(props) {
    const { name, items, initial }  = props;
    return (
      <select name={name} id={'id_' + name} className="select form-control">
        <option value="">{initial}</option>
        {items.map((i, index) =>
          <Choices key={index} inner={i[0]} outer={i[1]} />
        )}
      </select>
    )
}
const FormGroup = ({ name, label, element }) =>
      <div className="form-group" id={"div_id_"+name}>
        <label htmlFor={"id_"+name}>{label}</label>
        <div>
          {element}
        </div>
      </div>
const FlairWrapper = ({ t }) =>
    <Select
      name="flair"
      items={ t.state.flair }
      initial="Search by post flair..."
/>
const Flair = ({ t }) =>
    <FormGroup name="flair" label="Flair" element={<FlairWrapper t={t} />}
/>

const CategoryWrapper = <Select
    name="category"
    items ={[['selftext','Text'],['fullsize','Images']]}
    initial="Show only posts with..."
/>
const Category = <FormGroup
    name="category"
    label="Selftext category"
    element={CategoryWrapper}
/>

const Input = ({ type, name, css_class, value }) =>
    <input type={type} name={name} className={css_class} id={'id_'+name} value={value} />

const SortAsc = <Input type="checkbox" name="sort_asc" css_class="checkboxinput custom-control-input" value="on" />
const Submit = ({ t }) =>
  <Input
    type="submit"
    name="input"
    css_class="btn btn-primary btn btn-secondary col-sm-12"
    value={ t.state.archives.length === 0 && document.readyState === "complete" ? "Reset" : "Search" }
  />

const TextInput = ({ name, label, placeholder, type, value, min }) =>
   <FormGroup
      name={name}
      label={label}
      element={<input type={type} name={name} placeholder={placeholder}
        className="textinput textTextInput form-control"
        id={"id_"+name} autoComplete={value} min={min}></input>}
    />
const CommentAuthor = <TextInput
    name="comment_author"
    label="Comment author"
    placeholder="With comments by..."
    type="text"
    value="on"
    min=""
/>
const CommentBody = <TextInput
    name="comment_body"
    label="Comment body"
    placeholder="Comments contain search term (matches exact)..."
    type="text"
    value="on"
    min=""
/>
const Selftext = <TextInput
    name="selftext"
    label="Selftext"
    placeholder="Post body includes (matches exact)..."
    type="text"
    value="on"
    min=""
/>
const Title = <TextInput
    name="title"
    label="Title"
    placeholder="Title contains..."
    type="text"
    value="on"
    min=""
/>
const Author = <TextInput
    name="author"
    label="Author"
    placeholder="Submitted by..."
    type="text"
    value="on"
    min=""
/>
const DatePicker = ({ name, label }) =>
    <TextInput
      name={name+"_date"}
      label={"Submitted "+label}
      placeholder=""
      type="date"
      value="off"
      min=""
/>
const FromDate = <DatePicker
    name="from"
    label="after"
/>
const ToDate = <DatePicker
    name="to"
    label="before"
/>
const Comments = <TextInput
    name="comments"
    label="Comments"
    placeholder="Total ≥..."
    type="number"
    min="1"
    value=""
/>
const RowWrapper = ({ outer, field1, field2 }) =>
    <div className={outer}>
      {field1}
      {field2}
    </div>
const Row1 = ({ t }) =>
    <RowWrapper
      outer="form-row row-cols-2"
      field1={<Flair t={t} />}
      field2={Author}
    />
const Row2 =
    <div className="form-row row-cols-1 row-cols-lg-2">
      <RowWrapper
        outer="form-row row-cols-2 row-cols-lg-2 mb-0"
        field1={FromDate}
        field2={ToDate}
      />
      <RowWrapper
        outer="form-row row-cols-lg-1 row-cols-1 mb-0"
        field1={Title}
        field2=""
      />
    </div>
const Row3 =
    <div className="form-row row-cols-1 row-cols-lg-2">
      <div className="form-row row-cols-2 row-cols-lg-2">
        <div className="col col-lg-3 mb-0 ml-n1">
        <RowWrapper
          outer="mr-n3"
          field1={Comments}
          field2=""
        />
        </div>
        <RowWrapper
          outer="col col-lg-9 offset-lg-1 mr-n1 ml-2 mb-0"
          field1={Category}
          field2=""
        />
     </div>
       <RowWrapper
          outer="form-row row-cols-lg-1 row-cols-1 mb-0"
          field1={Selftext}
          field2=""
       />
    </div>
const Row4 = <RowWrapper
    outer="form-row row-cols-2 mb-0"
    field1={CommentAuthor}
    field2={CommentBody}
/>
const Row5 = ({ t }) =>
    <div  className="form-row">
      <div className="col col-sm-12 col-md-4 ml-n1 mb-0">
        <div className="form-group">
          <div id="div_id_sort_asc" className="custom-control custom-checkbox">
            {SortAsc}
            <label htmlFor="id_sort_asc" className="custom-control-label">
              Show oldest posts first
            </label>
          </div>
        </div>
      </div>
      <RowWrapper
        outer="col col-md-4 col-sm-12 mb-0"
        field1={<Submit t={t} />}
        field2=""
      />
    </div>

const Form = ({ t }) =>
    <form method="get">
      <div id="filter">
        <Row1 t={t} />
        {Row2}
        {Row3}
        {Row4}
        <Row5 t={t} />
      </div>
    </form>

export default Form;
