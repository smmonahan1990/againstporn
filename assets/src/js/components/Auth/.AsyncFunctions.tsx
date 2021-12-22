import { useForm } from "react-hook-form";
import useAuth from "./useAuth";
import Loading from "../App/Loading";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { useState } from 'react';

async function loginUser(credentials) {
  const url = "http://34.225.127.212/api/accounts/login/";
  const api_url =
    process.env.NODE_ENV === "production"
      ? url
      : url.replace("/api", ":8000/api");
  return fetch(api_url,{
    method: 'POST',
    headers: {
     'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
    })
   .then(function(data) {
      return data.json();
    })
   .catch((err) => console.log(err));
}

async function signupUser(credentials) {
  const url = "http://34.225.127.212/api/accounts/signup/";
  const api_url =
    process.env.NODE_ENV === "production"
      ? url
      : url.replace("/api", ":8000/api");
  return fetch(api_url,{
    method: 'POST',
    headers: {
     'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
    })
   .then(function(data) {
      return data.json();
    })
   .catch((err) => console.log(err));
}

import { useState, useEffect, createContext } from "react";
import type { AuthData, ModeHandler, AuthContextData } from "./AuthContext";
import AsyncLocalStorage from "@react-native-async-storage/async-storage";

export const AuthContext = createContext<AuthContextData>(
  {} as AuthContextData
);
async function logoutUser(token) {
    const url = "http://34.225.127.212/api/accounts/logout/";
    const api_url = 
        process.env.NODE_ENV === 'production' 
        ? url 
        : url.replace('/api', ':8000/api');
    return fetch(api_url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + JSON.parse(token).token
        },
    }).then(function(data) {
        return data.json();
    })
    .catch((err) => console.log(err));
}

async function checkStatus(suffix: string, data: string) {
    const url = 'http://34.225.127.212/api/accounts/' + suffix;
    const api_url = 
        process.env.NODE_ENV === 'production'
        ? url 
        : url.replace('/api', ':8000/api');
    return fetch(api_url, {
        method: 'GET',
        headers: {
           'Content-Type': 'application/json',
        }, 
        body: data
    }).then((response) => response.json()
    ).catch((err) => console.log(err));
}

async function resetPassword(data) {
  const url = "http://34.225.127.212/api/accounts/password/reset/";
  const api_url =
    process.env.NODE_ENV === "production"
      ? url
      : url.replace("/api", ":8000/api");
  return fetch(api_url,{
    method: 'POST',
    headers: {
     'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
    })
   .then(function(data) {
      return data.json();
    })
   .catch((err) => console.log(err));
}

async function passwordResetVerified(data) {
  const url = "http://34.225.127.212/api/accounts/password/reset/";
  const api_url =
    process.env.NODE_ENV === "production"
      ? url
      : url.replace("/api", ":8000/api");
  return fetch(api_url,{
    method: 'POST',
    headers: {
     'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
    })
   .then(function(data) {
      return data.json();
    })
   .catch((err) => console.log(err));
}
