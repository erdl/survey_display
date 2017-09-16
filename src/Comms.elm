module Comms exposing (..)
import Json.Decode as Jd
import Json.Encode as Je
import Types exposing (..)
import Dict exposing (Dict)
import Debug
import Http



-- shorthand record describing the fundamental 
-- units of a server communication.
type alias Comm a msg =
  { send : Server
  , read : Jd.Decoder a
  , wrap : ( Result Http.Error a -> msg )
  }

-- generic function for pushing a value to a server.
push : Comm a msg -> Je.Value  -> Cmd msg
push comm value =
  let
    body = Http.jsonBody value
  in
    Http.post comm.send body comm.read
    |> Http.send comm.wrap


-- generic function for pulling some value from a server.
pull : Comm a msg -> Cmd msg
pull comm =
  Http.get comm.send comm.read
  |> Http.send comm.wrap


-- pull a survey spec from the server.
pull_survey : Config -> Cmd Msg
pull_survey config =
  let
    wrap = (\ rslt ->
        Recv ( Update rslt )
        )
  in
    pull
      { send = config.srvr
      , read = jd_deployment
      , wrap = wrap
      }


-- push an archive to the server.
push_archive : Config -> Archive -> Cmd Msg
push_archive config arch =
  let
    data = je_archive arch
    comm =
      { send = config.srvr
      , read = Jd.succeed ()
      , wrap = (\ rslt ->
        Recv ( Upload rslt ) )
      }
  in
    push comm data


-- process a server response, possibly generating a `Pgrm`.
process_rsp : Maybe Pgrm -> Config -> Rsp -> Maybe (Pgrm,Config)
process_rsp pgrm conf rsp = 
  case pgrm of
    -- if `pgrm` exists, `rsp`.
    Just pgrm ->
      case rsp of
        Update deployment ->
          Just ( apply_update pgrm conf deployment )
        
        Upload rsp ->
          Just ( assess_upload pgrm rsp , conf )

    -- if no `pgrm` supplied, we are in `Init` case.
    Nothing ->
      case rsp of
        -- attempt to initialize the pgrm.
        Update rsp ->
          initialize_pgrm conf rsp
        -- anything other than an update is an error.
        _  ->
          let _ = Debug.log "unexpected comms" rsp
          in Nothing


-- attempt to generate a new pgrm instance from a server response.
initialize_pgrm : Config -> Result Http.Error Deployment -> Maybe (Pgrm,Config)
initialize_pgrm conf result =
  case result of
    Ok spec ->
      let
        conf_new = { conf | mode = spec.mode , code = spec.code }
        pgrm_new =
          { spec = spec.pgrm
          , sess = Dict.empty
          , arch = []
          }
      in
        Just ( pgrm_new , conf_new )
        
    Err err ->
      let _ = Debug.log "http error" err
      in Nothing


-- apply the new survey spec to `pgrm` if possible.
apply_update : Pgrm -> Config -> Result Http.Error Deployment -> (Pgrm,Config)
apply_update pgrm conf result =
  case result of
    Ok(spec) ->
      ( { pgrm | spec = spec.pgrm , sess = Dict.empty }
      , { conf | mode = spec.mode , code = spec.code  }
      )
    Err(error) ->
      let _ = Debug.log "error: " error
      in ( pgrm , conf )

-- assess the result of an upload attempt, and dispose
-- of the corresponding archive if able.
assess_upload : Pgrm -> Result Http.Error () -> Pgrm
assess_upload pgrm result =
  case result of
    Ok (rsp) ->
      let _ = Debug.log "upload ok" rsp
      in { pgrm | arch = [] }

    Err (err) ->
      let _ = Debug.log "upload err" err
      in pgrm


-- encodes an archive list to a json value.
je_archive : Archive -> Je.Value
je_archive arch =
  let
    responses = List.map je_response arch
  in
    Je.list responses


-- encodes a response record to a json value.
je_response : Response -> Je.Value
je_response rsp =
  let
    time = Je.int rsp.time
    suid = Je.int rsp.suid
    uuid = Je.int rsp.uuid
    sels = Je.list ( List.map je_selection rsp.sels )
  in
    Je.object
      [ ( "time" , time )
      , ( "suid" , suid )
      , ( "uuid" , uuid )
      , ( "sels" , sels )
      ]


-- encodes a selection record to a json value.
je_selection : Selection -> Je.Value
je_selection sel =
  let
    itm = Je.int sel.itm
    opt = Je.int sel.opt
  in
    Je.object
      [ ( "itm" , itm )
      , ( "opt" , opt )
      ]


-- decodes a json string into a deployment spec.
jd_deployment : Jd.Decoder Deployment
jd_deployment =
  let
    mode = Jd.map (\ bool ->
      case bool of
        True -> Kiosk
        False -> Form
      )  ( Jd.field "is-kiosk" Jd.bool )
    code = Jd.field "url-id" Jd.int
    pgrm = Jd.field "survey" jd_survey
  in
    Jd.map3 Deployment mode code pgrm

-- decodes a json string into a survey spec.
jd_survey : Jd.Decoder Survey
jd_survey =
  let
    text = Jd.field "text"   Jd.string
    code = Jd.field "code"   Jd.int
    itms = Jd.field "itms" ( Jd.list jd_question )
  in
    Jd.map3 Survey text code itms


-- decodes a json string into a question spec.
jd_question : Jd.Decoder Question
jd_question =
  let
    text = Jd.field "text" Jd.string
    code = Jd.field "code" Jd.int
    opts = Jd.field "opts" ( Jd.list jd_option )
  in
    Jd.map3 Question text code opts


-- decodes a json string into an option spec.
jd_option : Jd.Decoder Option
jd_option =
  let
    text = Jd.field "text" Jd.string
    code = Jd.field "code" Jd.int
  in
    Jd.map2 Option text code
