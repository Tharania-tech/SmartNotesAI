import React, { useState } from "react";
import {
  ArrowRight,
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
  UserRound,
  BookOpen
} from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import "./Login.css";

export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);

  const [rememberMe, setRememberMe] = useState(false);

  const [loading, setLoading] = useState(false);

  const [errorMessage, setErrorMessage] = useState("");

  /*
   * Flask backend URL.
   *
   * If VITE_API_BASE_URL exists in your .env file,
   * that value will be used.
   *
   * Otherwise the local Flask backend will be used.
   */
  const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL ||
    "http://127.0.0.1:5000/api";

  /*
   * -------------------------------------------------------
   * GET RESPONSE DATA
   * -------------------------------------------------------
   */
  function getResponseData(responseData) {
    if (
      responseData &&
      responseData.data &&
      typeof responseData.data === "object"
    ) {
      return responseData.data;
    }

    return responseData || {};
  }

  /*
   * -------------------------------------------------------
   * GET BACKEND ERROR MESSAGE
   * -------------------------------------------------------
   */
  function getErrorMessage(data) {
    if (
      data &&
      data.message
    ) {
      return String(data.message);
    }

    if (
      data &&
      data.error
    ) {
      return String(data.error);
    }

    if (
      data &&
      data.msg
    ) {
      return String(data.msg);
    }

    return "Unable to login. Please check your email and password.";
  }

  /*
   * -------------------------------------------------------
   * LOGIN
   * -------------------------------------------------------
   */
  async function handleSubmit(event) {
    event.preventDefault();

    const cleanEmail = email.trim();

    if (!cleanEmail) {
      setErrorMessage(
        "Please enter your email address."
      );
      return;
    }

    if (!password) {
      setErrorMessage(
        "Please enter your password."
      );
      return;
    }

    setLoading(true);
    setErrorMessage("");

    try {
      /*
       * ---------------------------------------------------
       * SEND LOGIN REQUEST TO FLASK
       *
       * POST
       * http://127.0.0.1:5000/api/auth/login
       *
       * Body:
       * {
       *   email: "...",
       *   password: "..."
       * }
       * ---------------------------------------------------
       */

      const response = await fetch(
        API_BASE_URL + "/auth/login",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            email: cleanEmail,
            password: password
          })
        }
      );

      /*
       * Try to read JSON response
       */
      let responseData = {};

      try {
        responseData = await response.json();
      } catch (jsonError) {
        responseData = {};
      }

      /*
       * If Flask returned 401 / 400 / 500 etc.
       */
      if (!response.ok) {
        setErrorMessage(
          getErrorMessage(responseData)
        );

        return;
      }

      /*
       * Extract response object
       */
      const data =
        getResponseData(responseData);

      /*
       * ---------------------------------------------------
       * SUPPORT DIFFERENT TOKEN FIELD NAMES
       * ---------------------------------------------------
       */

      let token = "";

      if (data.token) {
        token = String(data.token);
      } else if (data.access_token) {
        token = String(data.access_token);
      } else if (data.jwt) {
        token = String(data.jwt);
      } else if (data.accessToken) {
        token = String(data.accessToken);
      }

      /*
       * Sometimes APIs return:
       *
       * {
       *   data: {
       *      token: "...",
       *      user: {...}
       *   }
       * }
       *
       * So check nested data too.
       */

      if (
        !token &&
        data.data &&
        typeof data.data === "object"
      ) {
        if (data.data.token) {
          token = String(
            data.data.token
          );
        } else if (data.data.access_token) {
          token = String(
            data.data.access_token
          );
        } else if (data.data.jwt) {
          token = String(
            data.data.jwt
          );
        }
      }

      /*
       * ---------------------------------------------------
       * GET USER
       * ---------------------------------------------------
       */

      let user = {};

      if (
        data.user &&
        typeof data.user === "object"
      ) {
        user = data.user;
      } else if (
        data.data &&
        data.data.user &&
        typeof data.data.user === "object"
      ) {
        user = data.data.user;
      }

      /*
       * ---------------------------------------------------
       * TOKEN REQUIRED
       * ---------------------------------------------------
       */

      if (!token) {
        console.error(
          "Login response did not contain a token:",
          responseData
        );

        setErrorMessage(
          "Login successful, but the server did not return an authentication token."
        );

        return;
      }

      /*
       * ---------------------------------------------------
       * SAVE TOKEN
       * ---------------------------------------------------
       */

      localStorage.setItem(
        "smartnotes-token",
        token
      );

      /*
       * ---------------------------------------------------
       * SAVE USER
       * ---------------------------------------------------
       */

      localStorage.setItem(
        "smartnotes-user",
        JSON.stringify(user)
      );

      /*
       * ---------------------------------------------------
       * REMEMBER ME
       * ---------------------------------------------------
       */

      if (rememberMe) {
        localStorage.setItem(
          "smartnotes-remember",
          "true"
        );
      } else {
        localStorage.removeItem(
          "smartnotes-remember"
        );
      }

      /*
       * ---------------------------------------------------
       * SUCCESS
       * ---------------------------------------------------
       */

      navigate("/dashboard");

    } catch (error) {
      console.error(
        "Login connection error:",
        error
      );

      /*
       * Network/backend unavailable
       */
      if (
        error &&
        error.name === "TypeError"
      ) {
        setErrorMessage(
          "Cannot connect to the SmartNotes AI backend. Make sure Flask is running on http://127.0.0.1:5000."
        );
      } else {
        setErrorMessage(
          "Unable to connect to the login server."
        );
      }

    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="smart-login-page">

      <main className="smart-login-wrapper">

        {/* ==================================================
            LEFT ILLUSTRATION
        ================================================== */}

        <section className="smart-login-illustration">

          <div className="smart-login-illustration-content">

            <span className="smart-login-mini-title">
              SMART LEARNING
            </span>

            <h1>
              Learn smarter.
              <br />
              <strong>
                Grow faster.
              </strong>
            </h1>

            <p>
              Turn your study materials into simple,
              interactive and personalized learning
              experiences with SmartNotes AI.
            </p>

          </div>


          {/* ==================================================
              SVG SCENE
          ================================================== */}

          <div className="smart-student-scene">

            <svg
              viewBox="0 0 700 500"
              className="smart-student-svg"
              role="img"
              aria-label="Student studying with SmartNotes AI"
            >

              {/* Sky background */}

              <circle
                cx="118"
                cy="80"
                r="55"
                fill="#d9f6fb"
              />

              <circle
                cx="590"
                cy="95"
                r="75"
                fill="#dff5fc"
              />


              {/* Clouds */}

              <g opacity="0.85">

                <path
                  d="M60 145
                     C78 121 108 121 127 140
                     C142 119 179 116 198 144
                     H222
                     C236 144 247 155 247 169
                     H52
                     C51 159 54 151 60 145Z"
                  fill="#f7fdff"
                />

                <path
                  d="M495 154
                     C510 133 537 130 554 148
                     C571 124 610 126 626 151
                     H651
                     C663 151 674 162 674 174
                     H490
                     C488 166 491 159 495 154Z"
                  fill="#f7fdff"
                />

              </g>


              {/* Ground */}

              <path
                d="M0 386
                   Q120 340 240 377
                   T470 372
                   T700 360
                   V500
                   H0Z"
                fill="#9ed7df"
              />

              <path
                d="M0 424
                   Q130 390 270 420
                   T500 414
                   T700 395
                   V500
                   H0Z"
                fill="#e7f8fa"
              />


              {/* Decorative plants */}

              <g>

                <path
                  d="M105 415 C96 357 104 320 116 285"
                  stroke="#174f69"
                  strokeWidth="5"
                  fill="none"
                  strokeLinecap="round"
                />

                <ellipse
                  cx="96"
                  cy="343"
                  rx="24"
                  ry="13"
                  fill="#08a6b5"
                  transform="rotate(-40 96 343)"
                />

                <ellipse
                  cx="130"
                  cy="321"
                  rx="24"
                  ry="13"
                  fill="#168bd7"
                  transform="rotate(34 130 321)"
                />

                <ellipse
                  cx="94"
                  cy="300"
                  rx="20"
                  ry="11"
                  fill="#23bcca"
                  transform="rotate(-32 94 300)"
                />

                <path
                  d="M79 420
                     H138
                     L129 447
                     H87Z"
                  fill="#243c83"
                />

              </g>


              <g>

                <path
                  d="M604 420
                     C607 369 600 327 591 290"
                  stroke="#17516c"
                  strokeWidth="5"
                  fill="none"
                  strokeLinecap="round"
                />

                <ellipse
                  cx="614"
                  cy="344"
                  rx="22"
                  ry="12"
                  fill="#08a6b5"
                  transform="rotate(39 614 344)"
                />

                <ellipse
                  cx="578"
                  cy="322"
                  rx="22"
                  ry="12"
                  fill="#168bd7"
                  transform="rotate(-33 578 322)"
                />

                <ellipse
                  cx="611"
                  cy="299"
                  rx="18"
                  ry="10"
                  fill="#23bcca"
                  transform="rotate(32 611 299)"
                />

              </g>


              {/* Books */}

              <g>

                <rect
                  x="105"
                  y="400"
                  width="155"
                  height="22"
                  rx="6"
                  fill="#143b78"
                />

                <rect
                  x="116"
                  y="378"
                  width="150"
                  height="22"
                  rx="6"
                  fill="#08a6b5"
                />

                <rect
                  x="125"
                  y="356"
                  width="145"
                  height="22"
                  rx="6"
                  fill="#168bd7"
                />

                <text
                  x="145"
                  y="372"
                  fontSize="10"
                  fontWeight="700"
                  fill="#ffffff"
                >
                  STUDY
                </text>

                <text
                  x="137"
                  y="394"
                  fontSize="10"
                  fontWeight="700"
                  fill="#ffffff"
                >
                  PRACTICE
                </text>

                <text
                  x="131"
                  y="416"
                  fontSize="10"
                  fontWeight="700"
                  fill="#ffffff"
                >
                  GROW
                </text>

              </g>


              {/* Chair */}

              <rect
                x="330"
                y="326"
                width="104"
                height="80"
                rx="15"
                fill="#eafcff"
              />

              <rect
                x="345"
                y="398"
                width="14"
                height="52"
                rx="7"
                fill="#174d70"
              />

              <rect
                x="407"
                y="398"
                width="14"
                height="52"
                rx="7"
                fill="#174d70"
              />


              {/* Girl hair */}

              <circle
                cx="388"
                cy="176"
                r="43"
                fill="#263d83"
              />

              <circle
                cx="417"
                cy="154"
                r="22"
                fill="#263d83"
              />


              {/* Girl face */}

              <ellipse
                cx="390"
                cy="190"
                rx="31"
                ry="37"
                fill="#ffb7a8"
              />


              {/* Hair front */}

              <path
                d="M361 178
                   Q370 137 406 148
                   Q421 153 424 174
                   Q404 162 388 168
                   Q378 174 361 178Z"
                fill="#263d83"
              />


              {/* Neck */}

              <rect
                x="377"
                y="218"
                width="25"
                height="25"
                rx="9"
                fill="#ffb7a8"
              />


              {/* Shirt */}

              <path
                d="M350 239
                   Q390 220 429 240
                   L462 334
                   Q442 358 413 354
                   H350
                   Q325 348 313 330
                   L335 250Z"
                fill="#08a6b5"
              />


              {/* Shirt highlight */}

              <path
                d="M377 239
                   Q398 230 419 243
                   L431 319
                   H370Z"
                fill="#19b9c5"
                opacity="0.65"
              />


              {/* Left arm */}

              <path
                d="M337 255
                   Q315 279 309 315
                   Q304 335 321 337
                   Q339 338 346 320
                   L367 275Z"
                fill="#08a6b5"
              />


              {/* Right arm */}

              <path
                d="M427 249
                   Q450 278 465 304
                   Q473 316 461 326
                   Q451 335 441 321
                   L414 285Z"
                fill="#08a6b5"
              />


              {/* Laptop */}

              <rect
                x="335"
                y="288"
                width="153"
                height="93"
                rx="7"
                fill="#8bb6e6"
                transform="rotate(-3 335 288)"
              />

              <rect
                x="346"
                y="299"
                width="131"
                height="67"
                rx="4"
                fill="#eaf8ff"
                transform="rotate(-3 346 299)"
              />


              {/* Laptop screen */}

              <rect
                x="355"
                y="309"
                width="112"
                height="48"
                rx="3"
                fill="#d7f6fa"
                transform="rotate(-3 355 309)"
              />

              <circle
                cx="409"
                cy="332"
                r="13"
                fill="#08a6b5"
              />

              <path
                d="M404 332
                   L408 336
                   L416 326"
                stroke="#ffffff"
                strokeWidth="3"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
              />


              {/* Laptop base */}

              <path
                d="M324 375
                   H494
                   L515 389
                   Q518 395 509 397
                   H320
                   Q311 395 324 375Z"
                fill="#163c73"
              />


              {/* Legs */}

              <path
                d="M361 348
                   Q371 367 368 406
                   L347 445
                   H374
                   L397 410
                   L403 355Z"
                fill="#263d83"
              />

              <path
                d="M407 351
                   Q424 370 438 403
                   L460 442
                   H487
                   L463 400
                   L440 349Z"
                fill="#263d83"
              />


              {/* Shoes */}

              <path
                d="M344 442
                   H380
                   Q388 449 375 455
                   H337
                   Q330 452 344 442Z"
                fill="#ffffff"
              />

              <path
                d="M453 439
                   H484
                   Q494 446 483 452
                   H448
                   Q442 448 453 439Z"
                fill="#ffffff"
              />


              {/* Speech bubble */}

              <g>

                <rect
                  x="172"
                  y="187"
                  width="145"
                  height="65"
                  rx="16"
                  fill="#ffffff"
                  stroke="#79cfdc"
                  strokeWidth="2"
                />

                <path
                  d="M217 252
                     L205 274
                     L247 252Z"
                  fill="#ffffff"
                  stroke="#79cfdc"
                  strokeWidth="2"
                />

                <circle
                  cx="204"
                  cy="216"
                  r="8"
                  fill="#168bd7"
                />

                <path
                  d="M201 216
                     L204 219
                     L210 211"
                  stroke="#ffffff"
                  strokeWidth="2"
                  fill="none"
                />

                <text
                  x="221"
                  y="216"
                  fontSize="11"
                  fontWeight="700"
                  fill="#102d5a"
                >
                  Learn with AI
                </text>

                <text
                  x="221"
                  y="234"
                  fontSize="8"
                  fill="#75879e"
                >
                  Your notes. Your journey.
                </text>

              </g>


              {/* AI badge */}

              <g>

                <rect
                  x="492"
                  y="204"
                  width="70"
                  height="43"
                  rx="13"
                  fill="#168bd7"
                />

                <text
                  x="528"
                  y="231"
                  textAnchor="middle"
                  fontSize="17"
                  fontWeight="800"
                  fill="#ffffff"
                >
                  AI
                </text>

              </g>


              {/* Sparkles */}

              <circle
                cx="291"
                cy="133"
                r="7"
                fill="#08a6b5"
                opacity="0.65"
              />

              <circle
                cx="556"
                cy="259"
                r="6"
                fill="#168bd7"
                opacity="0.55"
              />

              <circle
                cx="275"
                cy="294"
                r="4"
                fill="#f3b84b"
                opacity="0.75"
              />

            </svg>

          </div>


          <div className="smart-illustration-tag">

            <BookOpen size={14} />

            <span>
              Study Smarter, Recall Faster
            </span>

          </div>

        </section>


        {/* ==================================================
            RIGHT LOGIN FORM
        ================================================== */}

        <section className="smart-login-form-panel">

          <div className="smart-login-top-link">

            <span>
              Don't have an account?
            </span>

            <Link to="/register">
              Register
              <ArrowRight size={14} />
            </Link>

          </div>


          <div className="smart-login-form-content">

            <div className="smart-login-heading">

              <span>
                WELCOME BACK
              </span>

              <h2>
                Login
              </h2>

              <p>
                Sign in to continue your SmartNotes AI
                learning journey.
              </p>

            </div>


            {errorMessage && (
              <div className="smart-login-error">
                {errorMessage}
              </div>
            )}


            <form
              className="smart-login-form"
              onSubmit={handleSubmit}
            >

              {/* EMAIL */}

              <div className="smart-field">

                <label htmlFor="email">
                  Email Address
                </label>

                <div className="smart-input">

                  <Mail size={18} />

                  <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={function (event) {
                      setEmail(
                        event.target.value
                      );

                      setErrorMessage("");
                    }}
                    placeholder="Enter your email"
                    autoComplete="email"
                  />

                </div>

              </div>


              {/* PASSWORD */}

              <div className="smart-field">

                <div className="smart-password-label">

                  <label htmlFor="password">
                    Password
                  </label>

                  <button
                    type="button"
                    onClick={function () {
                      window.alert(
                        "Password reset can be connected to your backend."
                      );
                    }}
                  >
                    Forgot password?
                  </button>

                </div>


                <div className="smart-input">

                  <LockKeyhole size={18} />

                  <input
                    id="password"
                    type={
                      showPassword
                        ? "text"
                        : "password"
                    }
                    value={password}
                    onChange={function (event) {
                      setPassword(
                        event.target.value
                      );

                      setErrorMessage("");
                    }}
                    placeholder="Enter your password"
                    autoComplete="current-password"
                  />

                  <button
                    type="button"
                    className="smart-eye"
                    onClick={function () {
                      setShowPassword(
                        !showPassword
                      );
                    }}
                    aria-label={
                      showPassword
                        ? "Hide password"
                        : "Show password"
                    }
                  >
                    {showPassword ? (
                      <EyeOff size={17} />
                    ) : (
                      <Eye size={17} />
                    )}
                  </button>

                </div>

              </div>


              {/* OPTIONS */}

              <div className="smart-login-options">

                <label>

                  <input
                    type="checkbox"
                    checked={rememberMe}
                    onChange={function (event) {
                      setRememberMe(
                        event.target.checked
                      );
                    }}
                  />

                  <span>
                    Remember me
                  </span>

                </label>

                <span className="smart-secure">
                  Secure Login
                </span>

              </div>


              {/* BUTTON */}

              <button
                type="submit"
                className="smart-login-button"
                disabled={loading}
              >

                <span>
                  {loading
                    ? "Signing in..."
                    : "Login"}
                </span>

                {loading ? (
                  <span className="smart-spinner"></span>
                ) : (
                  <ArrowRight size={18} />
                )}

              </button>

            </form>


            {/* Bottom register */}

            <div className="smart-login-bottom">

              <span>
                New to SmartNotes AI?
              </span>

              <Link to="/register">
                Create Account
              </Link>

            </div>

          </div>


          <div className="smart-login-footer">

            <span>
              SmartNotes AI
            </span>

            <span>
              •
            </span>

            <span>
              Your personalized learning workspace
            </span>

          </div>

        </section>

      </main>

    </div>
  );
}