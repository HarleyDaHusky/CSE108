// Calculator.js
import React, {useState, ReactDOM} from 'react';
import { Container, Grid, Button, TextField } from '@mui/material';
import './App.css';
var button;
var sincePreviousCalculations = 0;
var operationCount = 0;

<div id = "app"></div>

function Calculator(props) {
  const [result, SetResult] = React.useState(props.initialValue || ''); //screen
  const [input, SetInput] = useState(''); //mathValue
  const [previous, SetPrevious] = useState('') //previous
  const [lastOperation, SetlastOperation] = useState('')
  const [prevOp, SetprevOp] = useState('false');
  const [operationSet, SetOperation] = useState('false');

  const handleClick = (value) => {
    sincePreviousCalculations++;
    if (prevOp === "true") {
      SetResult(value);
      SetInput(input + value);
      SetprevOp('false');
      SetPrevious(value);
    }
    else {
      SetResult(result + value);
      SetInput(input + value);
      SetPrevious(value);
    }
  };

  const handleOperation = (value) => {
    sincePreviousCalculations++;
    if (operationSet === 'false') {
      if (value == '/') {
        button = document.getElementById('operation1');
        button.classList.add('highlight');
        SetlastOperation(value);
        sincePreviousCalculations++;
      }
      else if (value == '*') {
        button = document.getElementById('operation2');
        button.classList.add('highlight');
        SetlastOperation(value);
        sincePreviousCalculations++;
      }
      else if (value == "-") {
        button = document.getElementById('operation3');
        button.classList.add('highlight');
        SetlastOperation(value);
        sincePreviousCalculations++;
      }
      else if (value == "+") {
        button = document.getElementById('operation4');
        button.classList.add('highlight');
        SetlastOperation(value);
        sincePreviousCalculations++;
      }
      SetOperation('true');
    }
    else { //(operationSet === 'true')
      button.classList.remove('highlight');
      if (value == '/') {
        button = document.getElementById('operation1');
        button.classList.add('highlight');
        SetlastOperation(value);
        sincePreviousCalculations++
      }
      else if (value == '*') {
        button = document.getElementById('operation2');
        button.classList.add('highlight');
        SetlastOperation(value);
        sincePreviousCalculations++;
      }
      else if (value == "-") {
        button = document.getElementById('operation3');
        button.classList.add('highlight');
        SetlastOperation(value);
        sincePreviousCalculations++;
      }
      else if (value == "+") {
        button = document.getElementById('operation4');
        button.classList.add('highlight');
        SetlastOperation(value);
        sincePreviousCalculations++;
      }
    }
    if(operationCount > 0){
      try{
        SetResult(eval(input).toString());
        SetInput(input + value);
        operationCount++;
        SetprevOp('true');
        SetlastOperation(value);
      }
      catch (error) {
        SetResult('Error');
      }
    }
    else{
      SetInput(input+value);
      operationCount++;
      SetprevOp('true');
      SetlastOperation(value);
    }
  }
  
  const handleCalculate = () => {
    // const [result, SetResult] = useState(''); //screen
    // const [input, SetInput] = useState(''); //mathValue
    // const [previous, SetPrevious] = useState('') //previous
    try {
      if (sincePreviousCalculations == 0) {
        SetInput(input + lastOperation + previous);
        SetResult(eval(input.toString()));
      }
      else {
        SetResult(eval(input.toString()));
        sincePreviousCalculations = 0;
      }
    }
    catch (error) {
      SetResult('Error');
    }
    button = document.getElementById('operation1');
    button.classList.remove('highlight');
    button = document.getElementById('operation2');
    button.classList.remove('highlight');
    button = document.getElementById('operation3');
    button.classList.remove('highlight');
    button = document.getElementById('operation4');
    button.classList.remove('highlight');
  };

  const handleClear = () => {
    SetResult('');
    SetInput('');
    SetPrevious('');
    SetlastOperation('');
    SetOperation('false');
    button = document.getElementById('operation1');
    button.classList.remove('highlight');
    button = document.getElementById('operation2');
    button.classList.remove('highlight');
    button = document.getElementById('operation3');
    button.classList.remove('highlight');
    button = document.getElementById('operation4');
    button.classList.remove('highlight');
  }

  return (
    <Container maxWidth="sm">
      <TextField
        className="expression-field"
        value={"A Simple Calculator"}
        variant="outlined"
        fullWidth
        disabled
        margin="normal"
    />
    <Grid container spacing={1}>
    <div className="calculator">
      <input type="text" value={result} readOnly />
      <button onClick={() => handleClear()} id='C'>C</button>
      <div className="buttons">
        <div>
          <button onClick={() => handleClick('7')} id='number'>7</button>
          <button onClick={() => handleClick('8')} id='number'>8</button>
          <button onClick={() => handleClick('9')} id='number'>9</button>
          <button onClick={() => handleOperation('/')} id='operation1'>/</button>
        </div>
          <button onClick={() => handleClick('4')} id='number'>4</button>
          <button onClick={() => handleClick('5')} id='number'>5</button>
          <button onClick={() => handleClick('6')} id='number'>6</button>
          <button onClick={() => handleOperation('*')} id='operation2'>*</button>
        <div>
          <button onClick={() => handleClick('1')} id='number'>1</button>
          <button onClick={() => handleClick('2')} id='number'>2</button>
          <button onClick={() => handleClick('3')} id='number'>3</button>
          <button onClick={() => handleOperation('-')} id='operation3'>-</button>
        </div>
          <button onClick={() => handleClick('0')} id='number'>0</button>
          <button onClick={() => handleClick('.')} id='number'>.</button>
          <button onClick={() => handleCalculate()} id='operation'>=</button>
          <button onClick={() => handleOperation('+')} id='operation4'>+</button>
      </div>
    </div>
    </Grid>
    </Container>
  );
}
// ReactDOM.render(
//   <Calculator title = "Simple Calculator" />,
//   document.getElementById('app')
// );

export default Calculator;