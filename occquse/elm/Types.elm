module Types exposing (..)
import Http
import Dict exposing (Dict)

-- the model represents the state of the application at any given time.
type alias Model =
  { pgrm : Proc Pgrm   -- state of the program
  , conf : Config      -- configurations for app behavior
  , page : Page
  }


-- the app-config contains persistent variables which describe internal
-- behavior of the app independent of the specific query being served.
type alias Config =
  { srvr : Server     -- callback uri
  , tick : Seconds    -- server comm interval
  , code : Uid        -- the url id of the deployment
  , mode : Mode       -- operating mode: Kiosk || Form
  }




-- the program describes the internal state of a survey instance.
type alias Pgrm =
  { spec : Survey     -- specification of the specific survey.
  , sess : Session    -- dict of selections made by user.
  , arch : Archive    -- list of previous completed sessions.
  }

-- an updated set of run values from the server.
type alias Deployment =
  { mode : Mode
  , code : Uid
  , pgrm : Survey
  }

type Page = Main | Splash String

-- mode of display for the running program.
type Mode = Kiosk | Form


-- enum abstracting over the process of running
-- some generic program.
type Proc p = Init | Run p | Fin


-- enum representing possible input events.
type Input = Select Selection | Submit


-- enum representing the possible responses that can be recieved from server.
type Rsp = Update ( Result Http.Error Deployment ) | Upload ( Result Http.Error () )

-- enum representing possible state-altering events.
type Msg = User Input | Recv Rsp | Save Response | Set Page


-- type alias to clarify when a list of responses
-- is an archive object.
type alias Archive = List Response

-- type alias to help clarify when an integer is
-- intended to be used as a unique identified.
type alias Uid  = Int

-- type alias to clarify when a string is intended
-- for display to the user.
type alias Txt = String

-- type alias to clarify when an int represents
-- a value in seconds.
type alias Seconds = Int

-- type alias to clarify when a string represents
-- the url of the host server.
type alias Server = String

-- type alias to clarify what a string represents
-- the color to be rendered as background-color on the option button
type alias HexColor = String

-- represents an option that may be selected as
-- the response to a given question.
type alias Option =
  { text : Txt
  , code : Uid
  }


-- represents a question and its possible responses.
type alias Question =
  { text : Txt
  , code : Uid
  , opts : List Option
  }


-- represents one or more questions grouped together.
type alias Survey =
  { text : Txt
  , code : Uid
  , itms : List Question
  }


-- represents a selection event.
type alias Selection =
  { itm : Uid
  , opt : Uid
  }


-- represents the state of an active session; specifically
-- which options the user has currently selected.
type alias Session = Dict Uid Selection

-- represents a completed session which has been timestamped
-- and is ready for upload to the server.
type alias Response =
  { time : Seconds
  , suid : Uid
  , uuid : Uid
  , sels : List Selection
  }
