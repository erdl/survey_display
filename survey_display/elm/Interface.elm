module Interface exposing (..)

import Html exposing (Html)
import Html.Attributes as Ha
import Types exposing (..)
import Dict exposing (Dict)
import Components as Cmp
import Utilities as Utils


-- generate a kiosk-style interface.
render_kiosk : Pgrm -> Html Msg
render_kiosk { spec, sess } =
  case List.head spec.itms of
    Just spec ->
      let
        question = Cmp.question spec Nothing
      in
        Html.div
          [ Ha.class "kiosk" ]
          [ question         ]

    Nothing ->
     Cmp.splash "no questions available at this time" 


-- generate a form-style interface.
render_form : Pgrm -> Html Msg
render_form { spec , sess } =
  let
    questions = form_questions sess spec.itms
    sub = Cmp.submit ( Utils.is_filled spec sess )
  in
    Html.div
      [ Ha.class "form" ]
      [ questions , sub ]


-- generate the questions for a form-style interface.
form_questions : Session -> List Question -> Html Msg
form_questions session questions =
  let
    generate = (\ spec ->
      Cmp.question spec
        ( case Dict.get spec.code session of
          Just selection -> Just selection.opt
          Nothing -> Nothing )
      )
  in
    Html.div
      [ Ha.class "form-questions"   ]
      ( List.map generate questions )


-- apply user input to the program state.
form_input : Pgrm -> Config -> Input -> ( Pgrm , Cmd Msg )
form_input pgrm conf input =
  case input of
    Select selection ->
      let
        updated = Utils.insert_selection selection pgrm
      in
        ( updated , Cmd.none )

    Submit ->
      let
        (updated,cmd) =
          case Utils.submit_session pgrm conf of
            Ok (pgrm,cmd) -> (pgrm,cmd)
            Err (_) ->
              ( Debug.log "invalid submit event" pgrm
              , Cmd.none )
      in
        ( updated , cmd )


kiosk_input : Pgrm -> Config -> Input -> ( Pgrm , Cmd Msg )
kiosk_input pgrm conf input =
  case input of
    Select selection ->
      let
        updated = Utils.insert_selection selection pgrm
      in
        case Utils.submit_session updated conf of
          Ok (pgrm,cmd) -> (pgrm,cmd)
          Err (_) ->
            ( Debug.log "invalid submit event" pgrm
            , Cmd.none
            )
    Submit ->
      let
        _ = Debug.log "unexpected `Submit` event during kiosk mode" pgrm
      in
        ( pgrm, Cmd.none )

