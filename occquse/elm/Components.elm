module Components exposing (..)

import Html.Attributes as Ha
import Html.Events as He
import Html exposing (Html)
import Types exposing (..)
import Dict exposing (Dict)

-- this module contains 'primitive' components that are
-- used to construct surveys.


-- simple splash page for text display.
splash : String -> Html Msg
splash text =
  Html.h2
    [ Ha.class "splash" ]
    [ Html.text text    ]


-- generate a question from a `Question` specification
-- and (if exists) the id of the currently selected option.
question : Question -> Maybe Uid -> Html Msg
question spec selected =
  let
    text = question_text spec.text
    opts = options spec.code spec.opts selected
  in
    Html.div
      [ Ha.classList [ ( "question", True ) ] ]
      [ text, opts ]


-- generate question text.
question_text : Txt -> Html Msg
question_text text =
  Html.h2
    [ Ha.classList [ ( "question-text", True ) ] ]
    [ Html.text text ]


-- accepts a question-id, list of options, and (if exists),
-- the id of the currently selected option.  Generates a div
-- containing a selector for each listed option.
options : Uid -> List Option -> Maybe Uid -> Html Msg
options parent opts selected =
  let
    is_selected = (\ oid ->
      case selected of
        Just uid ->
          uid == oid
        Nothing -> False )
    mkSelector = (\ opt ->
      selector
        { itm = parent , opt = opt.code }
        opt.text
        ( is_selected opt.code )
      )
  in
    Html.div
      [ Ha.classList [ ( "options", True ) ] ]
      ( List.map mkSelector opts )


-- generate a button which fires off a `Submit` event.
-- Button only active/available when arg is `True`.
submit : Bool -> Html Msg
submit active =
  Html.button
    [ He.onClick ( User Submit )
    , Ha.class "submit-button"
    , Ha.disabled ( not active )
    ]
    [ Html.text "submit" ]


-- generic action button; accepts a tuple of the
-- form (class,text), as well as the `Input` message
-- to fire on a click event, and bool indicating if the
-- button is currently active/enabled.
actor : ( String , String ) -> Input -> Bool -> Html Msg
actor ( class , text ) input active =
  Html.button
    [ He.onClick ( User input )
    , Ha.class class
    , Ha.disabled ( not active )
    ]
    [ Html.text text ]


-- generate a button which fires off a `Selection`
-- event when clicked, and can have it's membership
-- in the `"selected"` class toggled with a bool.
selector : Selection -> Txt -> Bool -> Html Msg
selector selection text selected =
  Html.button
    [ He.onClick ( User ( Select selection ) )
    , Ha.classList
      [ ( "selected" , selected )
      , ( "selector" , True   ) ]
    ]
    [ Html.text text ]


