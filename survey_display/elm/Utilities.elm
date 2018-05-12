module Utilities exposing (..)

import Types exposing (..)
import Time exposing (Time)
import Dict exposing (Dict)
import Task exposing (Task)


-- accepts a closure which converts `Time` to some
-- `msg`, generating a command to get current time. 
timestamp : ( Time -> msg ) -> Cmd msg
timestamp closure =
  Task.perform closure Time.now


-- attempt to execute a submit!
submit_session : Pgrm -> Config ->  Result () ( Pgrm , Cmd Msg )
submit_session pgrm conf =
  let
      save = (\ time ->
        Save
          { time = floor ( Time.inSeconds time )
          , suid = pgrm.spec.code
          , uuid = conf.code 
          , sels = Dict.values pgrm.sess
          } )
  in
    case conf.mode of
      Form ->
        if is_filled pgrm.spec pgrm.sess then
          Ok
            ( { pgrm | sess = Dict.empty }
            , timestamp save )

        else Err ()

      Kiosk ->
        Ok
          ( { pgrm | sess = Dict.empty }
          , timestamp save )


-- check if all options have been selected in a given session.
is_filled : Survey -> Session -> Bool
is_filled survey session =
  let
    fltr = (\item bool ->
      if bool then
        Dict.member item.code session
      else False )
  in
    List.foldr fltr True survey.itms


insert_selection : Selection -> Pgrm -> Pgrm
insert_selection selection pgrm =
  let
    sess = Dict.insert selection.itm selection pgrm.sess
  in
    { pgrm | sess = sess }


add_response : Response -> Pgrm -> Pgrm
add_response response pgrm =
  let
    arch = pgrm.arch ++ [ response ]
  in
    { pgrm | arch = arch }

