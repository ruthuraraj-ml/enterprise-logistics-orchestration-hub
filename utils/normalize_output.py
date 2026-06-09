import json


def normalize_output(result):

    if isinstance(result, dict):
        return result

    if hasattr(result, "json_dict"):
        if result.json_dict:
            return result.json_dict

    if hasattr(result, "raw"):

        raw = result.raw.strip()

        raw = raw.replace("```json", "")
        raw = raw.replace("```", "")
        raw = raw.strip()

        try:
            return json.loads(raw)

        except Exception as e:
            print("JSON PARSE FAILED")
            print(e)
            print(raw)

            return {"raw_output": raw}

    return {"raw_output": str(result)}