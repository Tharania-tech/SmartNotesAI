import React, {
  useEffect,
  useState
} from "react";

import {
  ArrowRight,
  FileText,
  Search,
  UploadCloud,
  BookOpen,
  Trash2
} from "lucide-react";

import {
  useNavigate
} from "react-router-dom";

import AppHeader from "../components/AppHeader";


import {
  getNotes
} from "../services/notesApi";

import "./MyNotes.css";


export default function MyNotes() {

  const navigate = useNavigate();


  // =========================================================
  // STATE
  // =========================================================

  const [notes, setNotes] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [searchText, setSearchText] =
    useState("");

  const [error, setError] =
    useState("");

  const [deletingNoteId, setDeletingNoteId] =
    useState("");


  // =========================================================
  // LOAD NOTES
  // =========================================================

  useEffect(
    function () {

      loadNotes();

    },
    []
  );


  async function loadNotes() {

    try {

      setLoading(true);

      setError("");


      const response =
        await getNotes();


      let noteList = [];


      // -----------------------------------------------------
      // RESPONSE IS ALREADY AN ARRAY
      // -----------------------------------------------------

      if (
        Array.isArray(response)
      ) {

        noteList =
          response;

      }


      // -----------------------------------------------------
      // RESPONSE = { notes: [...] }
      // -----------------------------------------------------

      else if (
        response &&
        Array.isArray(
          response.notes
        )
      ) {

        noteList =
          response.notes;

      }


      // -----------------------------------------------------
      // RESPONSE = { data: [...] }
      // -----------------------------------------------------

      else if (
        response &&
        Array.isArray(
          response.data
        )
      ) {

        noteList =
          response.data;

      }


      setNotes(
        noteList
      );


    } catch (err) {

      console.error(
        "My Notes error:",
        err
      );

      setError(
        "Unable to load your notes."
      );

      setNotes([]);


    } finally {

      setLoading(false);

    }

  }


  // =========================================================
  // GET NOTE ID
  // =========================================================

  function getNoteId(note) {

    if (!note) {
      return "";
    }


    // -----------------------------------------------------
    // MongoDB ObjectId returned as _id
    // -----------------------------------------------------

    if (
      note._id
    ) {

      return String(
        note._id
      );

    }


    // -----------------------------------------------------
    // Generic id
    // -----------------------------------------------------

    if (
      note.id
    ) {

      return String(
        note.id
      );

    }


    // -----------------------------------------------------
    // Backend note_id
    // -----------------------------------------------------

    if (
      note.note_id
    ) {

      return String(
        note.note_id
      );

    }


    return "";

  }


  // =========================================================
  // GET NOTE TITLE
  // =========================================================

  function getNoteTitle(note) {

    if (!note) {
      return "Untitled Note";
    }


    if (
      note.title
    ) {

      return String(
        note.title
      );

    }


    if (
      note.file_name
    ) {

      return String(
        note.file_name
      );

    }


    if (
      note.filename
    ) {

      return String(
        note.filename
      );

    }


    return "Untitled Note";

  }


  // =========================================================
  // GET NOTE DATE
  // =========================================================

  function getNoteDate(note) {

    let value = "";


    if (
      note.created_at
    ) {

      value =
        note.created_at;

    }

    else if (
      note.uploaded_at
    ) {

      value =
        note.uploaded_at;

    }


    if (!value) {

      return "Recently added";

    }


    try {

      const date =
        new Date(value);


      if (
        Number.isNaN(
          date.getTime()
        )
      ) {

        return "Recently added";

      }


      return date.toLocaleDateString(
        "en-IN",
        {
          day: "2-digit",
          month: "short",
          year: "numeric"
        }
      );


    } catch (err) {

      return "Recently added";

    }

  }


  // =========================================================
  // OPEN NOTE
  // =========================================================

  function openNote(note) {

    const noteId =
      getNoteId(note);


    // -----------------------------------------------------
    // NEVER navigate to /undefined
    // -----------------------------------------------------

    if (!noteId) {

      console.error(
        "Unable to open note. Note ID is missing:",
        note
      );

      setError(
        "Unable to open this note because its note ID is missing."
      );

      return;

    }


    console.log(
      "Opening note:",
      noteId
    );


    navigate(
      "/notes/" +
      noteId
    );

  }


  // =========================================================
  // DELETE NOTE
  // =========================================================

  async function deleteNote(note) {

    const noteId =
      getNoteId(note);


    // -----------------------------------------------------
    // NOTE ID REQUIRED
    // -----------------------------------------------------

    if (!noteId) {

      console.error(
        "Unable to delete note. Note ID is missing:",
        note
      );

      setError(
        "Unable to delete this note because its note ID is missing."
      );

      return;

    }


    const title =
      getNoteTitle(note);


    // -----------------------------------------------------
    // CONFIRM DELETE
    // -----------------------------------------------------

    const confirmed =
      window.confirm(
        'Are you sure you want to delete "' +
        title +
        '"?'
      );


    if (!confirmed) {
      return;
    }


    try {

      setError("");

      setDeletingNoteId(
        noteId
      );


      // ---------------------------------------------------
      // GET TOKEN
      // ---------------------------------------------------

      const token =
        localStorage.getItem(
          "smartnotes-token"
        );


      // ---------------------------------------------------
      // API BASE URL
      // ---------------------------------------------------

      const apiBaseUrl =
        import.meta.env.VITE_API_BASE_URL ||
        "http://127.0.0.1:5000/api";


      // ---------------------------------------------------
      // DELETE REQUEST
      // ---------------------------------------------------

      const response =
        await fetch(
          apiBaseUrl +
          "/notes/" +
          noteId,
          {
            method: "DELETE",

            headers: token
              ? {
                  Authorization:
                    "Bearer " +
                    token
                }
              : {}
          }
        );


      // ---------------------------------------------------
      // READ RESPONSE
      // ---------------------------------------------------

      let data = {};

      try {

        data =
          await response.json();

      } catch (jsonError) {

        data = {};

      }


      // ---------------------------------------------------
      // CHECK RESPONSE
      // ---------------------------------------------------

      if (
        !response.ok
      ) {

        throw new Error(
          data.message ||
          data.error ||
          "Unable to delete note."
        );

      }


      // ---------------------------------------------------
      // REMOVE NOTE FROM UI IMMEDIATELY
      // ---------------------------------------------------

      setNotes(
        function(previousNotes) {

          return previousNotes.filter(
            function(item) {

              return (
                getNoteId(item) !==
                noteId
              );

            }
          );

        }
      );


      console.log(
        "Note deleted successfully:",
        noteId
      );


    } catch (err) {

      console.error(
        "Delete note error:",
        err
      );


      setError(
        err &&
        err.message
          ? err.message
          : "Unable to delete note."
      );


    } finally {

      setDeletingNoteId(
        ""
      );

    }

  }


  // =========================================================
  // FILTER NOTES
  // =========================================================

  const filteredNotes =
    notes.filter(
      function (note) {

        const title =
          getNoteTitle(
            note
          ).toLowerCase();


        const search =
          searchText
            .trim()
            .toLowerCase();


        if (!search) {
          return true;
        }


        return title.includes(
          search
        );

      }
    );


  // =========================================================
  // RENDER
  // =========================================================

  return (

    <div className="my-notes-page">


      {/* =====================================================
          HEADER
      ===================================================== */}

      <AppHeader />


      <main className="my-notes-main">


        {/* ===================================================
            HERO
        =================================================== */}

        <section className="my-notes-hero">

          <div>

            <span className="my-notes-kicker">

              STUDY LIBRARY

            </span>


            <h1>
              My Notes
            </h1>


            <p>
              Keep all your uploaded study
              material organized in one place.
            </p>

          </div>


          <button
            type="button"
            className="my-notes-upload-button"
            onClick={
              function () {

                navigate(
                  "/upload"
                );

              }
            }
          >

            <UploadCloud
              size={17}
            />

            Upload New Notes

            <ArrowRight
              size={16}
            />

          </button>

        </section>


        {/* ===================================================
            SEARCH TOOLBAR
        =================================================== */}

        <section className="my-notes-toolbar">

          <div className="my-notes-search">

            <Search
              size={17}
            />

            <input
              type="text"
              placeholder="Search your notes..."
              value={searchText}
              onChange={
                function (event) {

                  setSearchText(
                    event.target.value
                  );

                }
              }
            />

          </div>


          <div className="my-notes-count">

            <FileText
              size={15}
            />

            {notes.length}

            {" "}

            {
              notes.length === 1
                ? "Note"
                : "Notes"
            }

          </div>

        </section>


        {/* ===================================================
            CONTENT
        =================================================== */}

        {loading ? (

          <section className="my-notes-state">

            <div className="my-notes-loader"></div>

            <h3>
              Loading your notes...
            </h3>

            <p>
              Preparing your study library.
            </p>

          </section>


        ) : error ? (

          <section className="my-notes-state">

            <div className="my-notes-state-icon">

              <FileText
                size={23}
              />

            </div>

            <h3>
              {error}
            </h3>

            <button
              type="button"
              onClick={
                function () {

                  loadNotes();

                }
              }
            >
              Try Again
            </button>

          </section>


        ) : filteredNotes.length === 0 ? (

          <section className="my-notes-empty">

            <div className="my-notes-empty-icon">

              <BookOpen
                size={25}
              />

            </div>


            <h2>

              {
                notes.length === 0
                  ? "Your study library is empty"
                  : "No matching notes found"
              }

            </h2>


            <p>

              {
                notes.length === 0
                  ? "Upload your first study note and start learning with SmartNotes AI."
                  : "Try another search term."
              }

            </p>


            {notes.length === 0 && (

              <button
                type="button"
                onClick={
                  function () {

                    navigate(
                      "/upload"
                    );

                  }
                }
              >

                <UploadCloud
                  size={17}
                />

                Upload Notes

              </button>

            )}

          </section>


        ) : (

          <section className="my-notes-grid">

            {
              filteredNotes.map(
                function (
                  note,
                  index
                ) {


                  // =========================================
                  // NOTE DATA
                  // =========================================

                  const noteId =
                    getNoteId(
                      note
                    );


                  const title =
                    getNoteTitle(
                      note
                    );


                  const date =
                    getNoteDate(
                      note
                    );


                  const isDeleting =
                    deletingNoteId ===
                    noteId;


                  return (

                    <article
                      className="my-note-card"
                      key={
                        noteId ||
                        index
                      }
                    >


                      {/* =====================================
                          CARD TOP
                      ====================================== */}

                      <div className="my-note-card-top">

                        <div className="my-note-icon">

                          <FileText
                            size={19}
                          />

                        </div>


                        <span className="my-note-type">

                          STUDY NOTE

                        </span>


                        {/* =================================
                            DELETE BUTTON
                        ================================== */}

                        <button
                          type="button"
                          className="my-note-delete"
                          title={
                            isDeleting
                              ? "Deleting note..."
                              : "Delete note"
                          }
                          aria-label={
                            "Delete " +
                            title
                          }
                          disabled={
                            isDeleting
                          }
                          onClick={
                            function (event) {

                              // Prevent the card action
                              // from being triggered.
                              event.stopPropagation();

                              deleteNote(
                                note
                              );

                            }
                          }
                        >

                          <Trash2
                            size={17}
                          />

                        </button>

                      </div>


                      {/* =====================================
                          NOTE CONTENT
                      ====================================== */}

                      <div className="my-note-content">

                        <h3
                          title={title}
                        >
                          {title}
                        </h3>


                        <p>
                          Uploaded {date}
                        </p>

                      </div>


                      {/* =====================================
                          OPEN NOTE
                      ====================================== */}

                      <button
                        type="button"
                        className="my-note-open"
                        disabled={
                          isDeleting
                        }
                        onClick={
                          function () {

                            openNote(
                              note
                            );

                          }
                        }
                      >

                        <span>

                          {
                            isDeleting
                              ? "Deleting..."
                              : "Open Note"
                          }

                        </span>

                        {
                          !isDeleting && (

                            <ArrowRight
                              size={16}
                            />

                          )
                        }

                      </button>


                    </article>

                  );

                }
              )
            }

          </section>

        )}

      </main>
      <Footer />
    </div>

  );

}