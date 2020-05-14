let _outputID = "";
let _minValue = null;
let _maxValue = null;
let _isInRange = true;

function show_easy_numpad(thisElement)
{
    let easy_numpad = document.createElement("div");
    easy_numpad.id = "easy-numpad-frame";
    easy_numpad.className = "easy-numpad-frame";
    easy_numpad.innerHTML = `
    <div class="easy-numpad-container">
        <div class="easy-numpad-output-container">
            <p class="easy-numpad-output" id="easy-numpad-output"></p>
        </div>
        <div class="easy-numpad-number-container">
            <table>
                <tr>
                    <td><a href="7" onclick="easynum(this)">7</a></td>
                    <td><a href="8" onclick="easynum(this)">8</a></td>
                    <td><a href="9" onclick="easynum(this)">9</a></td>
                    <td><a href="Del" class="del" id="del" onclick="easy_numpad_del()">Del</a></td>
                </tr>
                <tr>
                    <td><a href="4" onclick="easynum(this)">4</a></td>
                    <td><a href="5" onclick="easynum(this)">5</a></td>
                    <td><a href="6" onclick="easynum(this)">6</a></td>
                    <td><a href="Clear" class="clear" id="clear" onclick="easy_numpad_clear()">Clear</a></td>
                </tr>
                <tr>
                    <td><a href="1" onclick="easynum(this)">1</a></td>
                    <td><a href="2" onclick="easynum(this)">2</a></td>
                    <td><a href="3" onclick="easynum(this)">3</a></td>
                    <td><a href="Cancel" class="cancel" id="cancel" onclick="easy_numpad_cancel()">Cancel</a></td>
                </tr>
                <tr>
                    <td><a href="±" onclick="easynum(this)">±</a></td>
					<td ><a href="0"onclick="easynum(this)">0</a></td>
                    <td><a href="." onclick="easynum(this)">.</a></td>
                    <td><a href="Done" class="done" id="done" onclick="easy_numpad_done()">Done</a></td>
                </tr>
            </table>
        </div>
    </div>
    `;

    document.getElementsByTagName('body')[0].appendChild(easy_numpad);
    _outputID = thisElement.id;
    _minValue = document.getElementById(thisElement.id).getAttribute("min");
    _maxValue = document.getElementById(thisElement.id).getAttribute("max");

    let useDefault = document.getElementById(thisElement.id).getAttribute("data-easynumpad-use_default");
    if(useDefault != "false")
    {
        document.getElementById("easy-numpad-output").innerText = thisElement.value;
    }
}

function easy_numpad_close()
{
        let elementToRemove = document.querySelectorAll("div.easy-numpad-frame")[0];
        elementToRemove.parentNode.removeChild(elementToRemove);
}

function easynum(thisElement)
{
    event.preventDefault();

    let currentValue = document.getElementById("easy-numpad-output").innerText;

    switch(thisElement.innerText)
    {
        case "±":
            if(currentValue.startsWith("-"))
            {
                document.getElementById("easy-numpad-output").innerText = currentValue.substring(1,currentValue.length);
            }
            else
            {
                document.getElementById("easy-numpad-output").innerText = "-" + currentValue;
            }
        break;
        case ".":
            if(_isInRange)
            {
                if(currentValue.length === 0)
                {
                    document.getElementById("easy-numpad-output").innerText = "0.";
                }
                else if(currentValue.length === 1 && currentValue === "-")
                {
                    document.getElementById("easy-numpad-output").innerText = currentValue + "0.";
                }
                else
                {
                    if(currentValue.indexOf(".") < 0)
                    {
                        document.getElementById("easy-numpad-output").innerText += ".";
                    }
                }
            }
        break;
        case "0":
            if(_isInRange)
            {
                if(currentValue.length === 0)
                {
                    document.getElementById("easy-numpad-output").innerText = "0.";
                }
                else if(currentValue.length === 1 && currentValue === "-")
                {
                    document.getElementById("easy-numpad-output").innerText = currentValue + "0.";
                }
                else
                {
                    document.getElementById("easy-numpad-output").innerText += thisElement.innerText;
                }
            }
        break;
        default:
            if(_isInRange)
            {
                document.getElementById("easy-numpad-output").innerText += thisElement.innerText;
            }
        break;
    }

    let newValue = Number(document.getElementById("easy-numpad-output").innerText);
    easy_numpad_check_range(newValue);
}

function easy_numpad_del()
{
    event.preventDefault();
    let easy_numpad_output_val = document.getElementById("easy-numpad-output").innerText;
    if(easy_numpad_output_val.slice(-2) !== "0." && easy_numpad_output_val.slice(-3) !== "-0.")
    {
        var easy_numpad_output_val_deleted = easy_numpad_output_val.slice(0, -1);
        document.getElementById("easy-numpad-output").innerText = easy_numpad_output_val_deleted;
        easy_numpad_check_range(Number(easy_numpad_output_val_deleted));
    }
}

function easy_numpad_clear()
{
    event.preventDefault();
    document.getElementById("easy-numpad-output").innerText="";
}

function easy_numpad_cancel()
{
    event.preventDefault();

    if(_isInRange)
    {
        easy_numpad_close();
    }
}

function easy_numpad_done()
{
    event.preventDefault();

    if(_isInRange)
    {
        let easy_numpad_output_val = document.getElementById("easy-numpad-output").innerText;

        if(easy_numpad_output_val.indexOf(".") === (easy_numpad_output_val.length - 1))
        {
            easy_numpad_output_val = easy_numpad_output_val.substring(0,easy_numpad_output_val.length - 1);
        }

        document.getElementById(_outputID).value = easy_numpad_output_val;
        el = document.getElementById(_outputID);
        ev = document.createEvent('Event');
        ev.initEvent('change', true, false);
        el.dispatchEvent(ev);
        easy_numpad_close();
    }
}

function easy_numpad_check_range(value)
{
    let outputElement = document.getElementById("easy-numpad-output");
    if(_maxValue != null && _minValue != null)
    {
        console.log("Range limit");

        if(value <= _maxValue && value >= _minValue)
        {
            outputElement.style.color = "black";
            _isInRange = true;
        }
        else
        {
            outputElement.style.color = "red";
            _isInRange = false;
        }
    }
    else if(_maxValue != null)
    {
        console.log("Only upper limit");

        if(value <= _maxValue)
        {
            outputElement.style.color = "black";
            _isInRange = true;
        }
        else
        {
            outputElement.style.color = "red";
            _isInRange = false;
        }
    }
    else if (_minValue != null)
    {
        console.log("Only lower limit");

        if(value >= _minValue)
        {
            outputElement.style.color = "black";
            _isInRange = true;
        }
        else
        {
            outputElement.style.color = "red";
            _isInRange = false;
        }
    }
    else
    {
        outputElement.style.color = "black";
        _isInRange = true;
    }
}
