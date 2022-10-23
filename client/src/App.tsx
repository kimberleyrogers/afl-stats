import React, { useEffect, useState} from "react";


const [data, setData] = useState("")

export function App() {

  useEffect(() => {
    fetch("/").then(
      res => res.json()
    )
    .then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])

  return  (
    <div>

      {/* {(typeof data.members === 'undefined') ? (
        <p>Loading...</p>
      ) : (
        data.members.map((member, i) => (
          <p key={i}>{member}</p>
        ))
      )} */}

      <p>Hello :)</p>

    </div>
  )
}

// module.exports;
// export = App;
