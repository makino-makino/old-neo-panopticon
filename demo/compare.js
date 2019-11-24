const fetch = require("node-fetch");

(async () => {
  const globalTL = await fetch("http://localhost:3001/api/posts?tl=global", {
    credentials: "omit",
    headers: {
      accept: "application/json",
      "accept-language": "ja,en;q=0.9",
      "access-token": "9kl26s8nugeCWqyP2lVOwA",
      client: "oNs64a4apjK6EU1BRqQhFA",
      "if-none-match": 'W/"c8ba61bc56d22c6e5d4ee9c7c66a564c"',
      "sec-fetch-mode": "cors",
      "sec-fetch-site": "same-origin",
      uid: "hoge@example.com"
    },
    referrer: "http://localhost:3001/globalTL",
    referrerPolicy: "no-referrer-when-downgrade",
    body: null,
    method: "GET",
    mode: "cors"
  }).then(res => {
    // resはResponseオブジェクト
    // console.log(res);
    // 返されたBodyをjsonにしてPromise.resolve()する
    return res.json();
  });

  const debugTL = await fetch("http://localhost:3001/api/posts?", {
    credentials: "omit",
    headers: {
      accept: "application/json",
      "accept-language": "ja,en;q=0.9",
      "access-token": "9kl26s8nugeCWqyP2lVOwA",
      client: "oNs64a4apjK6EU1BRqQhFA",
      "if-none-match": 'W/"fb764211e6d81fe8972885b2ada2f59a"',
      "sec-fetch-mode": "cors",
      "sec-fetch-site": "same-origin",
      uid: "hoge@example.com"
    },
    referrer: "http://localhost:3001/debugTL",
    referrerPolicy: "no-referrer-when-downgrade",
    body: null,
    method: "GET",
    mode: "cors"
  }).then(res => {
    // resはResponseオブジェクト
    // console.log(res);
    // 返されたBodyをjsonにしてPromise.resolve()する
    return res.json();
  });

  var globalSum = 0;
  var debugSum = 0;

  for (const index in globalTL) {
    const globalPost = globalTL[index];
    const debugPost = debugTL[index];

    globalSum += globalPost.total_evaluation;
    debugSum += debugPost.total_evaluation;
  }

  console.log(`global sum: ${globalSum}`);
  console.log(`debug sum: ${debugSum}`);
})();
