import { Question } from "./types.ts";

function parseQuestion(lines: string) {
  return lines.split("~~").map((lines) => {
    const split = lines.trim().split("\r\n");
    const length = split.length;
    if (length < 6) {
      return null;
    }
    const title_split = split[length - 6].split(" ");
    const id = title_split[0];
    const correct = title_split[1].at(1);
    const description = title_split[2] || "";
    const question = split[length - 5];
    const answers = split.slice(length - 4, length).map((line) =>
      line.replace(/^[A-D]\. /, "")
    );
    const figure = question.match(/[fF]igure [TGE](?:-[1-9]|[1-9]-[1-9])/)?.[0].slice(7).toLowerCase() || "";
    return {
      id,
      correct,
      question,
      answers,
      description,
      figure,
    } as Question;
  });
}

async function main() {
  for await (const file of Deno.readDir("./original")) {
    const data = await Deno.readTextFile(`./original/${file.name}`);
    const questions = parseQuestion(data).filter(Boolean);
    // save to json
    await Deno.writeTextFile(
      `./parsed/${file.name.replace(".txt", ".json")}`,
      JSON.stringify(questions, null, 2)
    );
  }
}

main();
