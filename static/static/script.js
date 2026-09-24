const taskSelect = document.getElementById("task");
const levelContainer = document.getElementById("level-container");
const levelSelect = document.getElementById("level");

const inputText = document.getElementById("input-text");
const characterCount = document.getElementById("character-count");

const submitButton = document.getElementById("submit-button");
const buttonText = document.getElementById("button-text");
const spinner = document.getElementById("spinner");

const resultSection = document.getElementById("result-section");
const resultTitle = document.getElementById("result-title");
const resultContent = document.getElementById("result-content");

const copyButton = document.getElementById("copy-button");


const taskInformation = {
    qa: {
        title: "Answer",
        placeholder:
            "Example: What is the difference between TCP and UDP?"
    },

    explain: {
        title: "Explanation",
        placeholder:
            "Example: Explain the Pythagoras theorem in simple words."
    },

    quiz: {
        title: "Quiz",
        placeholder:
            "Paste a topic or study passage here to generate a quiz."
    },

    summarize: {
        title: "Summary",
        placeholder:
            "Paste the educational passage you want to summarize."
    },

    learn: {
        title: "Learning Path",
        placeholder:
            "Example: I want to learn SQL from beginner to advanced."
    }
};


taskSelect.addEventListener("change", () => {

    const task = taskSelect.value;

    inputText.placeholder =
        taskInformation[task].placeholder;

    if (task === "learn") {
        levelContainer.classList.remove("hidden");
    } else {
        levelContainer.classList.add("hidden");
    }

    clearResult();
});


inputText.addEventListener("input", () => {

    characterCount.textContent =
        inputText.value.length;
});


submitButton.addEventListener("click", async () => {

    const task = taskSelect.value;

    const text = inputText.value.trim();

    if (!text) {
        showError(
            "Please enter a question, topic, or study material."
        );

        return;
    }

    if (text.length > 20000) {
        showError(
            "Please keep your input below 20,000 characters."
        );

        return;
    }

    setLoading(true);

    try {

        let endpoint;
        let body;

        if (task === "qa") {

            endpoint = "/qa";

            body = {
                question: text
            };

        } else if (task === "explain") {

            endpoint = "/explain";

            body = {
                text: text
            };

        } else if (task === "quiz") {

            endpoint = "/quiz";

            body = {
                text: text
            };

        } else if (task === "summarize") {

            endpoint = "/summarize";

            body = {
                text: text
            };

        } else if (task === "learn") {

            endpoint = "/learn/recommendations";

            body = {
                topic: text,
                level: levelSelect.value
            };

        }


        const response = await fetch(
            endpoint,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(body)
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Something went wrong."
            );

        }


        displayResult(task, data.result);

    } catch (error) {

        showError(
            error.message ||
            "Unable to connect to EduGenie."
        );

    } finally {

        setLoading(false);

    }
});


function setLoading(isLoading) {

    submitButton.disabled = isLoading;

    if (isLoading) {

        buttonText.textContent =
            "Generating...";

        spinner.classList.remove("hidden");

    } else {

        buttonText.textContent =
            "Start Learning";

        spinner.classList.add("hidden");

    }
}


function displayResult(task, result) {

    resultSection.classList.remove("hidden");

    resultTitle.textContent =
        taskInformation[task].title;

    resultContent.innerHTML = "";


    if (task === "quiz") {

        renderQuiz(result);

    } else {

        const textElement =
            document.createElement("div");

        textElement.className =
            "result-text";

        textElement.textContent =
            result;

        resultContent.appendChild(
            textElement
        );

    }


    resultSection.scrollIntoView({
        behavior: "smooth"
    });
}


function renderQuiz(quiz) {

    if (!quiz || !quiz.questions) {

        showError(
            "Quiz data was not returned correctly."
        );

        return;
    }


    let score = 0;

    let answered = 0;

    const questions =
        quiz.questions;


    const scoreElement =
        document.createElement("div");

    scoreElement.className =
        "quiz-score";

    scoreElement.textContent =
        "Answer all questions to see your score.";

    resultContent.appendChild(
        scoreElement
    );


    questions.forEach(
        (item, questionIndex) => {

            const questionCard =
                document.createElement("div");

            questionCard.className =
                "quiz-question";


            const heading =
                document.createElement("h3");

            heading.textContent =
                `${questionIndex + 1}. ${item.question}`;

            questionCard.appendChild(
                heading
            );


            item.options.forEach(
                (option) => {

                    const optionElement =
                        document.createElement("div");

                    optionElement.className =
                        "quiz-option";

                    optionElement.textContent =
                        option;

                    optionElement.dataset.answer =
                        option;

                    optionElement.addEventListener(
                        "click",
                        () => {

                            if (
                                questionCard.dataset.answered ===
                                "true"
                            ) {
                                return;
                            }


                            questionCard.dataset.answered =
                                "true";

                            answered++;


                            const isCorrect =
                                option ===
                                item.correct_answer;


                            if (isCorrect) {

                                score++;

                                optionElement.classList.add(
                                    "correct"
                                );

                            } else {

                                optionElement.classList.add(
                                    "incorrect"
                                );


                                const allOptions =
                                    questionCard.querySelectorAll(
                                        ".quiz-option"
                                    );


                                allOptions.forEach(
                                    (element) => {

                                        if (
                                            element.dataset.answer ===
                                            item.correct_answer
                                        ) {

                                            element.classList.add(
                                                "correct"
                                            );

                                        }

                                    }
                                );

                            }


                            const feedback =
                                document.createElement(
                                    "div"
                                );

                            feedback.className =
                                "quiz-feedback";

                            feedback.textContent =
                                isCorrect
                                    ? `Correct! ${item.explanation}`
                                    : `Correct answer: ${item.correct_answer}. ${item.explanation}`;

                            questionCard.appendChild(
                                feedback
                            );


                            updateScore(
                                scoreElement,
                                score,
                                answered,
                                questions.length
                            );

                        }
                    );


                    questionCard.appendChild(
                        optionElement
                    );

                }
            );


            resultContent.appendChild(
                questionCard
            );

        }
    );
}


function updateScore(
    element,
    score,
    answered,
    total
) {

    if (answered < total) {

        element.textContent =
            `Score: ${score}/${total} — ${answered}/${total} answered.`;

    } else {

        element.textContent =
            `Final Score: ${score}/${total}`;
    }
}


function showError(message) {

    resultSection.classList.remove("hidden");

    resultTitle.textContent =
        "Error";

    resultContent.innerHTML = "";


    const errorElement =
        document.createElement("div");

    errorElement.className =
        "error";

    errorElement.textContent =
        message;


    resultContent.appendChild(
        errorElement
    );


    resultSection.scrollIntoView({
        behavior: "smooth"
    });
}


function clearResult() {

    resultSection.classList.add(
        "hidden"
    );

    resultContent.innerHTML = "";
}


copyButton.addEventListener(
    "click",
    async () => {

        try {

            await navigator.clipboard.writeText(
                resultContent.innerText
            );

            copyButton.textContent =
                "Copied!";

            setTimeout(
                () => {
                    copyButton.textContent =
                        "Copy";
                },
                1500
            );

        } catch {

            copyButton.textContent =
                "Copy failed";

        }

    }
);
