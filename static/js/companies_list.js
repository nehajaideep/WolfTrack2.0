class StatusCellRenderer {
  eGui;

  init(params) {
    const eGui = (this.eGui = document.createElement("div"));
    eGui.style.overflow = "hidden";
    eGui.style.textOverflow = "ellipsis";

    const { value } = params;
    const statusSpan = document.createElement("span");
    const text = document.createTextNode(value ?? "");

    if (value != null) {
      statusSpan.style.borderLeft = "10px solid " + params.value;
      statusSpan.style.paddingRight = "5px";
    }

    eGui.appendChild(statusSpan);
    eGui.append(text);
  }

  getGui() {
    return this.eGui;
  }

  refresh() {
    return false;
  }
}

const status_values = ["Wishlist", "Applied", "In Progress", "Offer"];

var filterParams = {
  comparator: (filterLocalDateAtMidnight, cellValue) => {
    var dateAsString = cellValue;
    if (dateAsString == null) return -1;
    var dateParts = dateAsString.split("/");
    var cellDate = new Date(
      Number(dateParts[2]),
      Number(dateParts[0]) - 1,
      Number(dateParts[1])
    );

    if (filterLocalDateAtMidnight.getTime() === cellDate.getTime()) {
      return 0;
    }

    if (cellDate < filterLocalDateAtMidnight) {
      return -1;
    }

    if (cellDate > filterLocalDateAtMidnight) {
      return 1;
    }
    return 0;
  },
  minValidYear: 2000,
  maxValidYear: 2023,
  inRangeFloatingFilterDateFormat: "MMM Do YYYY",
};

const columnDefs = [
  {
    headerName: "Company",
    field: "company",
    editable: true,
    resizable: false,
    sortable: true,
    filter: true,
  },
  {
    headerName: "Status",
    field: "status",
    cellRenderer: StatusCellRenderer,
    cellEditor: "agSelectCellEditor",
    cellEditorParams: {
      values: status_values,
    },
    sortable: true,
    filter: true,
  },
  {
    headerName: "Application Date",
    field: "applicationdate",
    filter: "agDateColumnFilter",
    filterParams: filterParams,
    editable: true,
    sortable: true,
  },
  {
    headerName: "Due Date",
    field: "duedate",
    editable: true,
    filter: "agDateColumnFilter",
    filterParams: filterParams,
    sortable: true,
  },
];

let data = JSON.parse(localStorage.getItem("jobApplications"));

if (!data) {
  data = [
    {
      company: "Amazon",
      status: status_values[0],
      applicationdate: "10/09/2023",
      duedate: "10/11/2023",
    },
    {
      company: "Cisco",
      status: status_values[1],
      applicationdate: "10/09/2023",
      duedate: "10/11/2023",
    },
    {
      company: "Adobe",
      status: status_values[2],
      applicationdate: "10/10/2023",
      duedate: "10/15/2023",
    },
    {
      company: "Notion",
      status: status_values[3],
      applicationdate: "10/10/2023",
      duedate: "10/16/2023",
    },
    {
      company: "Branch",
      status: status_values[0],
      applicationdate: "10/10/2023",
      duedate: "10/16/2023",
    },
  ];

  localStorage.setItem("jobApplications", JSON.stringify(data));
}

const saveChanges = () => {
  localStorage.setItem("jobApplications", JSON.stringify(updatedData));
};
var updatedData = [];
const gridOptions = {
  defaultColDef: {
    flex: 1,
    resizable: true,
    editable: true,
  },
  columnDefs: columnDefs,
  rowData: data,
  onCellValueChanged: function (event) {
    gridOptions.api.forEachNode((node) => {
      updatedData.push({
        company: node.data.company,
        status: node.data.status,
        applicationdate: node.data.applicationdate,
        duedate: node.data.duedate,
      });
    });
  },
};

document.addEventListener("DOMContentLoaded", () => {
  const gridDiv = document.querySelector("#myGrid");
  const urlSearchParams = new URLSearchParams(window.location.search);
  const status = urlSearchParams.get("status");
  const decodedStatus = decodeURIComponent(status);
  new agGrid.Grid(gridDiv, gridOptions);
  gridOptions.api.setQuickFilter(decodedStatus);
  
  // Calculate the count of job applications with today's date
  const today = new Date();
  const todayDateString = `${today.getMonth() + 1}/${today.getDate()}/${today.getFullYear()}`;
  const applied = data.filter((jobApplication) => jobApplication.applicationdate === todayDateString).length;



  const addNewCompany = (company, status, applicationDate, dueDate) => {
    const newCompany = {
      company,
      status,
      applicationdate: applicationDate,
      duedate: dueDate,
    };
    data.push(newCompany);
    updatedData.push(newCompany);
    saveChanges();
    gridOptions.api.setRowData(data);
  };
});
