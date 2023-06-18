import React, { useState, useEffect } from "react";
import "./CardsStyles.css";

import Card from "./Card";

// https://www.youtube.com/watch?v=hEtZ040fsD8&feature=youtu.be&t=719 (flashcards)
// https://www.youtube.com/watch?v=vs6usnS5OTE (slider)

export default function Cards() {
  const [flashcarddata, setFlashcarddata] = useState([]);

  useEffect(() => {
    const url =
      "https://api.airtable.com/v0/appqY5UZYlf41Q5VT/Table%201?api_key=keyPZ9SKzXIt4Ek1v";
    fetch(url)
      .then((response) => response.json())
      .then((json) => {
        setFlashcarddata(json.records);
      }, []);
  });

  // https://www.debuggr.io/react-map-of-undefined/
  const cards = flashcarddata.map((card) => {
    return <Card card={card} key={card.id} />;
  });

  const loading = <div className="loading">Loading flashcard content...</div>;

  // navigation in cards
  const [current, setCurrent] = useState(0);
  function previousCard() {
    setCurrent(current - 1);
  }
  function nextCard() {
    setCurrent(current + 1);
  }

  // if (flashcarddata) {
  //   return (
  //     <div>
  //       <div>The number of cards is: {flashcarddata.length}</div>
  //       {cards[0]}
  //     </div>
  //   );
  // } else {
  //   return <div>Loading...</div>;
  // }
  return (
    <div>
      {/* number of cards */}
      {flashcarddata && flashcarddata.length > 0 ? (
        <div className="cardNumber">
          Card {current + 1} of {flashcarddata.length}
        </div>
      ) : (
        ""
      )}
      {/* /number of cards */}

      {/* render cards */}
      {flashcarddata && flashcarddata.length > 0 ? cards[current] : loading}
      {/* /render cards */}

      {/* render nav buttons */}
      <div className="nav">
        {current > 0 ? (
          <button onClick={previousCard}>Previous card</button>
        ) : (
          <button className="disabled" disabled>
            Previous card
          </button>
        )}
        {current < flashcarddata.length - 1 ? (
          <button onClick={nextCard}>Next card</button>
        ) : (
          <button className="disabled" disabled>
            Next card
          </button>
        )}
        {/* /render nav buttons */}
      </div>
    </div>
  );
}
