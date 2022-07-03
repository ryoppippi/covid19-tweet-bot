const P_URL =
  "https://data.corona.go.jp/converted-json/covid19japan-npatients.json";
const D_URL =
  "https://data.corona.go.jp/converted-json/covid19japan-ndeaths.json";

const downloadData = async <T>(url: string) => {
  const response = await fetch(url);
  const data = (await response.json()) as T;
  return data;
};

const getPatientData = async () =>
  await downloadData<
    Array<{
      date: string;
      npatients: number;
      adpatients: number;
    }>
  >(P_URL);

const getDeathData = async () =>
  await downloadData<
    Array<{
      date: string;
      ndeaths: number;
    }>
  >(D_URL);

const compareWithCache = async (msg: string, previousFilename: string) => {
  try {
    const previousMsg = await Deno.readTextFile(previousFilename);
    return msg === previousMsg;
  } catch (e) {
    return false;
  }
};

const writeCache = async (msg: string, filename: string) => {
  try {
    await Deno.writeTextFile(filename, msg);
  } catch (e) {
    throw new Error(e);
  }
  return true;
};

const genMsg = async () => {
  const [deathData, patientData] = await Promise.all([
    getDeathData(),
    getPatientData(),
  ]);
  const todaysData = {
    death: [...deathData].reverse()[0],
    patient: [...patientData].reverse()[0],
  };
  const yesterdayData = {
    death: [...deathData].reverse()[1],
    patient: [...patientData].reverse()[1],
  };

  const msg = `新型コロナウイルス国内感染の状況
${todaysData.death.date} 現在
感染者: ${todaysData.patient.npatients}名
死者: ${todaysData.death.ndeaths}名
感染者は前日から ${todaysData.patient.adpatients}名増加しました
死者は前日から ${
    todaysData.death.ndeaths - yesterdayData.death.ndeaths
  }名増加しました
詳しくはこちら↓
corona.go.jp/dashboard
#新型コロナ #Covid_19`;
  return msg;
};

const sendTweet = async (msg: string) => {
  const webhookAccessKey = Deno.env.get("webhook_access_key");
  const iftttEvent = "create_tweet";

  const url = new URL(
    `https://maker.ifttt.com/trigger/${iftttEvent}/with/key/${webhookAccessKey}`
  );
  url.searchParams.append("value1", msg);
  const resp = await fetch(url);
  if (!resp.ok) {
    throw new Error(resp.statusText);
  }
  return resp;
};

const main = async () => {
  const msg = await genMsg();
  console.log(msg);
  if (await compareWithCache(msg, "./tweet/DTWEET.txt")) {
    console.log("No update");
    return;
  }
  const resp = await sendTweet(msg).catch(console.error);
  if (resp && resp.ok) {
    return (
      (await writeCache(msg, "./tweet/DTWEET.txt").catch(console.error)) &&
      console.log("Done")
    );
  }
};

await main();
