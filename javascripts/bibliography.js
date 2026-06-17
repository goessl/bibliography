var url = new URL('../bibliography.json', window.location.href).href;

fetch(url)
  .then(function(response) { return response.json(); })
  .then(function(data) {

//autocolumns would only scan first row
var allFields = new Set(data.flatMap(Object.keys));
var priority = ['type', 'id', 'author', 'editor', 'title', 'subtitle', 'date', 'note', 'edition', 'publisher', 'isbn', 'doi', 'url'];
var fields = [
  ...priority.filter(function(f) { return allFields.has(f); }),
  ...[...allFields].filter(function(f) { return !priority.includes(f); })
];
var persons = [...new Set(data.flatMap(function (e) { return e.author || e.editor || []; }))].sort();

//define formatting and filtering for each column
var columns = fields.map(function (field) {
  var column = {title: field,
                field: field };
  
  switch (field) {
    case "type":
      column.headerFilter = "list";
      column.headerFilterParams = {valuesLookup: true,
                                   clearable: true,
                                   multiselect: true };
      column.headerFilterFunc = "in";
      break;
    
    case "author":
    case "editor":
      column.formatter = function (cell) {
        var values = cell.getValue() || [];
        return (
          "<ul>" +
          values.map(function (a) { return "<li>"+a+"</li>"; }).join("") +
          "</ul>"
        );
      };
      column.headerFilter = "list";
      column.headerFilterParams = {values: persons, clearable: true, multiselect: true};
      column.headerFilterFunc = function (headerValue, rowValue) {
        if (!headerValue || !headerValue.length) return true;
        return (rowValue || []).some(function (a) { return headerValue.includes(a); });
      };
      break;
    
    case "url":
      column.formatter = "link";
      column.formatterParams = {label: "link",
                                target: "_blank" };
      break;
    
    case "publisher":
      column.headerFilter = "list";
      column.headerFilterParams = {valuesLookup: true,
                                   clearable: true,
                                   multiselect: true };
      column.headerFilterFunc = "in";
      break;
    
    case "doi":
      column.formatter = "link";
      column.formatterParams = {
        label: function (cell) { return cell.getValue(); },
        url: function (cell) { return "https://doi.org/" + cell.getValue(); },
        target: "_blank"
      };
      column.headerFilter = "input";
      break;
    
    default:
      column.headerFilter = "input";
      break;
  }
  
  return column;
});

new Tabulator("#bibliography-table", {
  data: data,
  columns: columns
});

});
