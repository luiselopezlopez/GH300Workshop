from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def calculate(num1, operator, num2):
    """Perform a basic arithmetic calculation and return the result."""
    if operator == "+":
        return num1 + num2
    elif operator == "-":
        return num1 - num2
    elif operator == "*":
        return num1 * num2
    elif operator == "/":
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        return num1 / num2
    elif operator == "sqr":
        return num1 * num1
    else:
        raise ValueError(f"Unknown operator: {operator}")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate_route():
    data = request.get_json()
    try:
        num1 = float(data["num1"])
        operator = data["operator"]
        num2 = float(data["num2"]) if operator != "sqr" else 0
        result = calculate(num1, operator, num2)
        # Return integer when result has no fractional part
        if result == int(result):
            result = int(result)
        return jsonify({"result": result})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except (KeyError, TypeError):
        return jsonify({"error": "Invalid input"}), 400


if __name__ == "__main__":
    app.run()
