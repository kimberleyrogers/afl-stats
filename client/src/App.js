"use strict";
exports.__esModule = true;
var react_1 = require("react");
var _a = (0, react_1.useState)(""), data = _a[0], setData = _a[1];
function App() {
    (0, react_1.useEffect)(function () {
        fetch("/").then(function (res) { return res.json(); }).then(function (data) {
            setData(data);
            console.log(data);
        });
    }, []);
    return;
    <div>

      {(typeof data.members === 'undefined') ? (<p>Loading...</p>) : (data.members.map(function (member, i) { return (<p key={i}>{member}</p>); }))}

    </div>;
}
exports["default"] = App;
