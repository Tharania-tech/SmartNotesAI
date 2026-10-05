import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import "./Register.css";

import Logo from "../components/Logo";

export default function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
    agreed: false,
  });

  const [showPassword, setShowPassword] =
    useState(false);

  const [errors, setErrors] =
    useState({});

  const [loading, setLoading] =
    useState(false);


  /* =========================================================
     HANDLE CHANGE
     ========================================================= */

  const handleChange = (e) => {
    const {
      name,
      value,
      type,
      checked,
    } = e.target;

    setForm((prev) => ({
      ...prev,
      [name]:
        type === "checkbox"
          ? checked
          : value,
    }));

    setErrors((prev) => ({
      ...prev,
      [name]: undefined,
      api: undefined,
    }));
  };


  /* =========================================================
     VALIDATION
     ========================================================= */

  const validate = () => {
    const next = {};

    if (
      form.name.trim().length < 3
    ) {
      next.name =
        "Name must contain at least 3 characters.";
    }

    if (!form.email.trim()) {
      next.email =
        "Please enter your email address.";
    } else if (
      !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
        form.email.trim()
      )
    ) {
      next.email =
        "Please enter a valid email address.";
    }

    if (
      form.password.length < 8
    ) {
      next.password =
        "Passwords need at least 8 characters.";
    }

    if (
      form.confirmPassword !==
      form.password
    ) {
      next.confirmPassword =
        "These two passwords don't match.";
    }

    if (!form.agreed) {
      next.agreed =
        "Accept the terms to continue.";
    }

    return next;
  };


  /* =========================================================
     API ERROR MESSAGE
     ========================================================= */

  const getErrorMessage = (error) => {

    if (
      error &&
      error.response &&
      error.response.data
    ) {

      const data =
        error.response.data;

      if (data.message) {
        return String(
          data.message
        );
      }

      if (data.error) {
        return String(
          data.error
        );
      }

      if (data.detail) {
        return String(
          data.detail
        );
      }
    }

    if (
      error &&
      error.message
    ) {
      return String(
        error.message
      );
    }

    return "Unable to connect to the backend.";
  };


  /* =========================================================
     REGISTER
     ========================================================= */

  const handleSubmit = async (e) => {

    e.preventDefault();

    const found =
      validate();

    setErrors(found);

    if (
      Object.keys(found).length > 0
    ) {
      return;
    }

    setLoading(true);

    try {

      console.log(
        "================================"
      );

      console.log(
        "REGISTER REQUEST"
      );

      console.log(
        "Name:",
        form.name
      );

      console.log(
        "Email:",
        form.email
      );

      /*
       * Send registration data
       * to Flask backend.
       *
       * Final URL:
       * http://127.0.0.1:5000/api/auth/register
       *
       * because api.js uses:
       * VITE_API_BASE_URL=http://127.0.0.1:5000/api
       */

      const response =
        await api.post(
          "/auth/register",
          {
            name:
              form.name.trim(),

            email:
              form.email.trim(),

            password:
              form.password
          },
          {
            timeout: 30000
          }
        );


      console.log(
        "Register response:",
        response
      );


      /* =====================================================
         GET BACKEND RESPONSE
         ===================================================== */

      let data = {};

      if (
        response &&
        response.data
      ) {
        data =
          response.data;
      }


      console.log(
        "Register response data:",
        data
      );


      /* =====================================================
         REGISTRATION SUCCESS
         ===================================================== */

      alert(
        data.message ||
        "Account created successfully. Please login."
      );


      /* =====================================================
         GO TO LOGIN PAGE
         ===================================================== */

      navigate("/login");


    } catch (error) {

      console.error(
        "================================"
      );

      console.error(
        "REGISTRATION ERROR"
      );

      console.error(
        error
      );

      console.error(
        "================================"
      );


      const message =
        getErrorMessage(
          error
        );


      setErrors({
        api: message
      });


      alert(
        message
      );


    } finally {

      setLoading(false);

    }
  };


  return (
    <div className="register">

      {/* ---------- Brand panel ---------- */}

      <aside className="register__brand">

        <div className="register__brand-inner">

          <header className="brand-head">
            <div className="brand-logo-card">
    <Logo />
  </div>
          </header>


          <div className="brand-copy">

            <span className="brand-badge">
              Smart learning
            </span>

            <h1 className="brand-title">

              Create your

              <br />

              learning space.

            </h1>

            <p className="brand-sub">

              Join SmartNotes AI and turn
              your study material into summaries,
              quizzes and a tutor that knows
              what you're revising.

            </p>

          </div>


          <ul className="brand-steps">

            <li className="brand-step brand-step--study">
              Study
            </li>

            <li className="brand-step brand-step--practice">
              Practice
            </li>

            <li className="brand-step brand-step--grow">
              Grow
            </li>

          </ul>


          <ul className="brand-chips">

            <li>
              Summaries
            </li>

            <li>
              Quizzes
            </li>

            <li>
              AI tutor
            </li>

          </ul>

        </div>


        {/* soft shapes */}

        <span
          className="orb orb--lg"
          aria-hidden="true"
        />

        <span
          className="orb orb--sm"
          aria-hidden="true"
        />

        <span
          className="spark"
          aria-hidden="true"
        >

          <svg
            viewBox="0 0 24 24"
            fill="currentColor"
          >

            <path d="M12 2l1.9 5.9L20 9.8l-5.2 3.2L15.6 19 12 15.6 8.4 19l.8-6L4 9.8l6.1-1.9L12 2z" />

          </svg>

        </span>


        {/* the curve that bites into the form side */}

        <svg
          className="brand-curve"
          viewBox="0 0 120 800"
          preserveAspectRatio="none"
          aria-hidden="true"
        >

          <path d="M0,0 C95,150 120,330 78,420 C36,510 5,640 40,800 L120,800 L120,0 Z" />

        </svg>

      </aside>


      {/* ---------- Form panel ---------- */}

      <main className="register__panel">

        <span
          className="blob blob--top"
          aria-hidden="true"
        />

        <span
          className="blob blob--bottom"
          aria-hidden="true"
        />


        <form
          className="card"
          onSubmit={handleSubmit}
          noValidate
        >

          <h2 className="card__title">
            Register
          </h2>

          <p className="card__eyebrow">
            Observe· Details Faster
          </p>


          {/* API ERROR */}

          {errors.api && (

            <span className="field__error field__error--block">

              {errors.api}

            </span>

          )}


          {/* NAME */}

          <label className="field">

            <input
              className={
                "field__input " +
                (
                  errors.name
                    ? "is-invalid"
                    : ""
                )
              }
              type="text"
              name="name"
              value={
                form.name
              }
              onChange={
                handleChange
              }
              placeholder="Name"
              autoComplete="name"
            />

            {errors.name && (

              <span className="field__error">

                {errors.name}

              </span>

            )}

          </label>


          {/* EMAIL */}

          <label className="field">

            <input
              className={
                "field__input " +
                (
                  errors.email
                    ? "is-invalid"
                    : ""
                )
              }
              type="email"
              name="email"
              value={
                form.email
              }
              onChange={
                handleChange
              }
              placeholder="Email"
              autoComplete="email"
            />

            {errors.email && (

              <span className="field__error">

                {errors.email}

              </span>

            )}

          </label>


          {/* PASSWORD */}

          <label className="field">

            <input
              className={
                "field__input " +
                (
                  errors.password
                    ? "is-invalid"
                    : ""
                )
              }
              type={
                showPassword
                  ? "text"
                  : "password"
              }
              name="password"
              value={
                form.password
              }
              onChange={
                handleChange
              }
              placeholder="Password"
              autoComplete="new-password"
            />

            <button
              type="button"
              className="field__toggle"
              onClick={() =>
                setShowPassword(
                  (value) =>
                    !value
                )
              }
            >

              {showPassword
                ? "Hide"
                : "Show"}

            </button>

            {errors.password && (

              <span className="field__error">

                {errors.password}

              </span>

            )}

          </label>


          {/* CONFIRM PASSWORD */}

          <label className="field">

            <input
              className={
                "field__input " +
                (
                  errors.confirmPassword
                    ? "is-invalid"
                    : ""
                )
              }
              type={
                showPassword
                  ? "text"
                  : "password"
              }
              name="confirmPassword"
              value={
                form.confirmPassword
              }
              onChange={
                handleChange
              }
              placeholder="Confirm password"
              autoComplete="new-password"
            />

            {errors.confirmPassword && (

              <span className="field__error">

                {
                  errors.confirmPassword
                }

              </span>

            )}

          </label>


          {/* TERMS */}

          <label className="consent">

            <input
              type="checkbox"
              name="agreed"
              checked={
                form.agreed
              }
              onChange={
                handleChange
              }
            />

            <span>

              I accept the{" "}

              <a href="/terms">
                terms of use
              </a>

            </span>

          </label>


          {errors.agreed && (

            <span className="field__error field__error--block">

              {errors.agreed}

            </span>

          )}


          {/* SUBMIT */}

          <button
            className="submit"
            type="submit"
            disabled={loading}
          >

            {loading
              ? "Creating account..."
              : "Create account"}

          </button>
          {/* LOGIN */}

          <p className="card__foot">

            Already have an account?

            <a href="/login">
              Log in
            </a>

          </p>


          {/* DIVIDER */}

          <div className="divider">

            <span>
              Or sign up with
            </span>

          </div>


          {/* SOCIALS */}

          <div className="socials">

            <button
              type="button"
              className="social"
              aria-label="Sign up with Google"
            >

              <svg
                viewBox="0 0 24 24"
                aria-hidden="true"
              >

                <path
                  fill="#4285F4"
                  d="M21.6 12.2c0-.7-.1-1.3-.2-1.9H12v3.7h5.4a4.6 4.6 0 0 1-2 3v2.5h3.2c1.9-1.7 3-4.3 3-7.3z"
                />

                <path
                  fill="#34A853"
                  d="M12 22c2.7 0 5-.9 6.6-2.5l-3.2-2.5c-.9.6-2 1-3.4 1-2.6 0-4.8-1.8-5.6-4.1H3.1v2.6A10 10 0 0 0 12 22z"
                />

                <path
                  fill="#FBBC05"
                  d="M6.4 13.9a6 6 0 0 1 0-3.8V7.5H3.1a10 10 0 0 0 0 9l3.3-2.6 3z"
                />

                <path
                  fill="#EA4335"
                  d="M12 5.9c1.5 0 2.8.5 3.8 1.5l2.8-2.8A10 10 0 0 0 3.1 7.5l3.3 2.6C7.2 7.7 9.4 5.9 12 5.9z"
                />

              </svg>

            </button>


            <button
              type="button"
              className="social"
              aria-label="Sign up with GitHub"
            >

              <svg
                viewBox="0 0 24 24"
                fill="#1b1f23"
                aria-hidden="true"
              >

                <path d="M12 2a10 10 0 0 0-3.2 19.5c.5.1.7-.2.7-.5v-1.8c-2.8.6-3.4-1.3-3.4-1.3-.5-1.2-1.1-1.5-1.1-1.5-.9-.6.1-.6.1-.6 1 .1 1.5 1 1.5 1 .9 1.6 2.4 1.1 3 .9.1-.7.4-1.1.6-1.4-2.2-.3-4.6-1.1-4.6-5 0-1.1.4-2 1-2.7-.1-.3-.4-1.3.1-2.7 0 0 .8-.3 2.7 1a9.4 9.4 0 0 1 5 0c1.9-1.3 2.7-1 2.7-1 .5 1.4.2 2.4.1 2.7.6.7 1 1.6 1 2.7 0 3.9-2.4 4.7-4.6 5 .4.3.7.9.7 1.9v2.8c0 .3.2.6.7.5A10 10 0 0 0 12 2z" />

              </svg>

            </button>


            <button
              type="button"
              className="social"
              aria-label="Sign up with X"
            >

              <svg
                viewBox="0 0 24 24"
                fill="#111"
                aria-hidden="true"
              >

                <path d="M17.5 3h3l-6.6 7.5L21.8 21h-5.9l-4.2-5.5L6.7 21H3.6l7-8L2.6 3h6l3.8 5 4.2-5zm-1 16h1.6L8.1 4.6H6.4L16.5 19z" />

              </svg>

            </button>


            <button
              type="button"
              className="social"
              aria-label="Sign up with Microsoft"
            >

              <svg
                viewBox="0 0 24 24"
                aria-hidden="true"
              >

                <path
                  fill="#F25022"
                  d="M3 3h8.5v8.5H3z"
                />

                <path
                  fill="#7FBA00"
                  d="M12.5 3H21v8.5h-8.5z"
                />

                <path
                  fill="#00A4EF"
                  d="M3 12.5h8.5V21H3z"
                />

                <path
                  fill="#FFB900"
                  d="M12.5 12.5H21V21h-8.5z"
                />

              </svg>

            </button>

          </div>




        </form>

      </main>

    </div>
  );
}