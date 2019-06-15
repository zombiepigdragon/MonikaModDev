default persistent.monika_reload = 0
default persistent.tried_skip = False
default persistent.monika_kill = True #Assume non-merging players killed monika.
default persistent.rejected_monika = None
default initial_monika_file_check = None
define modoorg.CHANCE = 20
define mas_battery_supported = False
define mas_in_intro_flow = False

# True means disable animations, False means enable
default persistent._mas_disable_animations = False

# affection hotfix for dates
default persistent._mas_bday_date_affection_fix = False

init -1 python in mas_globals:
    # global that are not actually globals.

    # True means we are in the dialogue workflow. False means not
    dlg_workflow = False

    show_vignette = False
    # TRue means show the vignette mask, False means no show

    show_lightning = False
    # True means show lightening, False means do not

    lightning_chance = 6
    lightning_s_chance = 10
    # lghtning chances

    show_s_light = False
    # set to True to show s easter egg.
    # NOTE: set to True during o31, and also during sayori easter egg
    # TODO: need to this

    text_speed_enabled = False
    # set to True if text speed is enabled

    in_idle_mode = False
    # set to True if in idle mode


init 970 python:
    import store.mas_filereacts as mas_filereacts

#    mas_temp_moni_chksum = None

    if persistent._mas_moni_chksum is not None:
#        mas_temp_moni_chksum = persistent._mas_moni_chksum

        # do check for monika existence
        store.mas_dockstat.init_findMonika(mas_docking_station)

        # check surprise party
        store.mas_dockstat.surpriseBdayCheck(mas_docking_station)

        # check if coming from TT
        store.mas_o31_event.mas_return_from_tt = (
            store.mas_o31_event.isTTGreeting()
        )


    postbday_ev = mas_getEV("mas_bday_postbday_notimespent")

    if (
            postbday_ev is not None
            and persistent._mas_long_absence
            and postbday_ev.conditional is not None
            and eval(postbday_ev.conditional)
        ):
        # reset the post bday event if users did long absence to skip the
        # event
        postbday_ev.conditional = None
        postbday_ev.action = None

    if postbday_ev is not None:
        del postbday_ev

    if mas_isMonikaBirthday():
        persistent._mas_bday_opened_game = True

    # quick fix for dates
    # NOTE: remove this in 089
#    if (
#            persistent._mas_bday_date_affection_gained >= 50 and
#            not persistent._mas_bday_date_affection_fix
#        ):
#        mas_gainAffection(50, bypass=True)
#        persistent._mas_bday_date_affection_fix = True

    # o31 costumes flag
    # we only enable costumes if you are not playing for the first time today.
    if persistent._mas_o31_costumes_allowed is None:
        first_sesh = persistent.sessions.get("first_session", None)
        if first_sesh is not None:
            # fresh players will have first session today
            persistent._mas_o31_costumes_allowed = (
                first_sesh.date() != mas_o31
            )

        else:
            # no first sesh? you are also fresh
            persistent._mas_o31_costumes_allowed = False


init -10 python:
    # create the idle mailbox
    class MASIdleMailbox(store.MASMailbox):
        """
        Spaceroom idle extension of the mailbox

        PROPERTIES:
            (no additional)

        See MASMailbox for properties
        """

        # NOTE: add keys here
        REBUILD_EV = 1
        # rebuilds the event list in idle

        DOCKSTAT_GRE_TYPE = 2
        # used by the bye_going_somewhere farewell as a type

        IDLE_MODE_CB_LABEL = 3
        # label to call when returning from idle mode

        SKIP_MID_LOOP_EVAL = 4
        # True if we want idle to skip mid loop eval once

        # end keys
       

        def __init__(self):
            """
            Constructor for the idle mailbox
            """
            super(MASIdleMailbox, self).__init__()


        # NOTE: add additoinal functions below when appropriate.
        def send_rebuild_msg(self):
            """
            Sends the rebuild message to the mailbox
            """
            self.send(self.REBUILD_EV, True)


        def get_rebuild_msg(self):
            """
            Gets rebuild message
            """
            return self.get(self.REBUILD_EV)


        def send_ds_gre_type(self, gre_type):
            """
            Sends greeting type to mailbox
            """
            self.send(self.DOCKSTAT_GRE_TYPE, gre_type)


        def get_ds_gre_type(self, default=None):
            """
            Gets dockstat greeting type

            RETURNS: None by default
            """
            result = self.get(self.DOCKSTAT_GRE_TYPE)
            if result is None:
                return default
            return result


        def send_idle_cb(self, cb_label):
            """
            Sends idle callback label to mailbox
            """
            self.send(self.IDLE_MODE_CB_LABEL, cb_label)


        def get_idle_cb(self):
            """
            Gets idle callback label
            """
            return self.get(self.IDLE_MODE_CB_LABEL)


        def send_skipmidloopeval(self):
            """
            Sends skip mid loop eval message to mailbox
            """
            self.send(self.SKIP_MID_LOOP_EVAL, True)


        def get_skipmidloopeval(self):
            """
            Gets skip midloop eval value
            """
            return self.get(self.SKIP_MID_LOOP_EVAL)
            

    mas_idle_mailbox = MASIdleMailbox()


image blue_sky = "mod_assets/blue_sky.jpg"
image monika_room = "images/cg/monika/monika_room.png"
image monika_day_room = "mod_assets/monika_day_room.png"
image monika_gloomy_room = "mod_assets/monika_day_room_rain.png"
image monika_room_highlight:
    "images/cg/monika/monika_room_highlight.png"
    function monika_alpha
image monika_bg = "images/cg/monika/monika_bg.png"
image monika_bg_highlight:
    "images/cg/monika/monika_bg_highlight.png"
    function monika_alpha
image monika_scare = "images/cg/monika/monika_scare.png"

image monika_body_glitch1:
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"
    0.15
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"
    1.00
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"
    0.15
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"

image monika_body_glitch2:
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"
    0.15
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"
    1.00
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"
    0.15
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"



image room_glitch = "images/cg/monika/monika_bg_glitch.png"


# spaceroom window positions
transform spaceroom_window_left:
    size (320, 180) pos (30, 200)

transform spaceroom_window_right:
    size (320, 180) pos (935, 200)

init python:

    import subprocess
    import os
    import eliza      # mod specific
    import datetime   # mod specific
    import battery    # mod specific
    import re
    import store.songs as songs
    import store.hkb_button as hkb_button
    import store.mas_globals as mas_globals
    therapist = eliza.eliza()
    process_list = []
    currentuser = None # start if with no currentuser
    if renpy.windows:
        try:
            process_list = subprocess.check_output("wmic process get Description", shell=True).lower().replace("\r", "").replace(" ", "").split("\n")
        except:
            pass
        try:
            for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
                user = os.environ.get(name)
                if user:
                    currentuser = user
        except:
            pass

    try:
        renpy.file("../characters/monika.chr")
        initial_monika_file_check = True
    except:
        #Monika will mention that you don't have a char file in ch30_main instead
        pass


    # name changes if necessary
    if not currentuser or len(currentuser) == 0:
        currentuser = persistent.playername
    if not persistent.mcname or len(persistent.mcname) == 0:
        persistent.mcname = currentuser
        mcname = currentuser
    else:
        mcname = persistent.mcname

    # check for battery support
    mas_battery_supported = battery.is_supported()

    # we need a new music channel for background audio (like rain!)
    # this uses the amb (ambient) mixer. 
    renpy.music.register_channel(
        "background",
        mixer="amb",
        loop=True,
        stop_on_mute=True,
        tight=True
    )

    # also need another verison of background for concurrency
    renpy.music.register_channel(
        "backsound",
        mixer="amb",
        loop=False,
        stop_on_mute=True
    )

    #Define new functions
    def show_dialogue_box():
        """
        Jumps to the topic promt menu
        """
        renpy.jump('prompt_menu')


    def pick_game():
        """
        Jumps to the pick a game workflow
        """
        renpy.jump('pick_a_game')


    def mas_getuser():
        """
        Attempts to get the current user

        RETURNS: current user if found, or None if not found
        """
        for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
            user = os.environ.get(name)
            if user:
                return user

        return None


    def mas_enable_quitbox():
        """
        Enables Monika's quit dialogue warning
        """
        global _confirm_quit
        _confirm_quit = True


    def mas_disable_quitbox():
        """
        Disables Monika's quit dialogue warning
        """
        global _confirm_quit
        _confirm_quit = False


    def mas_enable_quit():
        """
        Enables quitting without monika knowing
        """
        persistent.closed_self = True
        mas_disable_quitbox()


    def mas_disable_quit():
        """
        Disables quitting without monika knowing
        """
        persistent.closed_self = False
        mas_enable_quitbox()


    def mas_drawSpaceroomMasks():
        """
        Draws the appropriate masks according to the current state of the
        game.

        ASSUMES:
            morning_flag
            mas_is_raining
            mas_is_snowing
        """
        # hide the existing masks
        renpy.hide("rm")
        renpy.hide("rm2")

        # get current weather masks
        left_w, right_w = mas_current_weather.sp_window(morning_flag)

        # should we use fallbacks instead?
        if persistent._mas_disable_animations:
            left_w += "_fb"
            right_w += "_fb"

        # now show the masks
        renpy.show(left_w, at_list=[spaceroom_window_left], tag="rm")
        renpy.show(right_w, at_list=[spaceroom_window_right], tag="rm2")


    def show_calendar():
        """RUNTIME ONLY
        Opens the calendar if we can
        """
        mas_HKBRaiseShield()

        if not persistent._mas_first_calendar_check:
            renpy.call('_first_time_calendar_use')

        renpy.call_in_new_context("mas_start_calendar_read_only")

        if store.mas_globals.in_idle_mode:
            # IDLe only enables talk extra and music
            store.hkb_button.talk_enabled = True
            store.hkb_button.extra_enabled = True
            store.hkb_button.music_enabled = True

        else:
            mas_HKBDropShield()


    dismiss_keys = config.keymap['dismiss']
    renpy.config.say_allow_dismiss = store.mas_hotkeys.allowdismiss

    def slow_nodismiss(event, interact=True, **kwargs):
        """
        Callback for whenever monika talks

        IN:
            event - main thing we can use here, lets us now when in the pipeline
                we are for display text:
                begin -> start of a say statement
                show -> right before dialogue is shown
                show_done -> right after dialogue is shown
                slow_done -> called after text finishes showing
                    May happen after "end"
                end -> end of dialogue (user has interacted)
        """
        # skip check
        # if config.skipping and not config.developer:
        #     persistent.tried_skip = True
        #     config.skipping = False
        #     config.allow_skipping = False
        #     renpy.jump("ch30_noskip")
        #     return

        if event == "begin":
            store.mas_hotkeys.allow_dismiss = False
#            config.keymap['dismiss'] = []
#            renpy.display.behavior.clear_keymap_cache()

        elif event == "slow_done":
            store.mas_hotkeys.allow_dismiss = True
#            config.keymap['dismiss'] = dismiss_keys
#            renpy.display.behavior.clear_keymap_cache()

    morning_flag = None
    def is_morning():
        # generate the times we need
        sr_hour, sr_min = mas_cvToHM(persistent._mas_sunrise)
        ss_hour, ss_min = mas_cvToHM(persistent._mas_sunset)
        sr_time = datetime.time(sr_hour, sr_min)
        ss_time = datetime.time(ss_hour, ss_min)

        now_time = datetime.datetime.now().time()

        return sr_time <= now_time < ss_time


    def mas_shouldRain():
        """
        Rolls some chances to see if we should make it rain

        RETURNS:
            rain weather to use, or None if we dont want to change weather
        """
        #All paths roll
        chance = random.randint(1,100)
        if mas_isMoniNormal(higher=True):
            #NOTE: Chances are as follows:
            #Spring:
            #   - Rain: 50%
            #   - Thunder: 20% (40% of that 50%)
            #
            #Summer:
            #   - Rain: 10%
            #   - Thunder: 6% (60% of that 10%)
            #
            #Fall:
            #   - Rain: 30%
            #   - Thunder: 12% (40% of that 50%)
            if mas_isSpring() and chance <= 50:
                if chance <= 20:
                    return mas_weather_thunder
                return mas_weather_rain

            elif mas_isSummer() and chance <= 10:
                if chance <= 6:
                    return mas_weather_thunder
                return mas_weather_rain

            elif mas_isFall() and chance <= 30:
                if chance <= 12:
                    return mas_weather_thunder
                return mas_weather_rain

        #Otherwise rain based on how Moni's feeling
        elif mas_isMoniUpset() and chance <= MAS_RAIN_UPSET:
            return mas_weather_rain

        elif mas_isMoniDis() and chance <= MAS_RAIN_DIS:
            return mas_weather_rain

        elif mas_isMoniBroken() and chance <= MAS_RAIN_BROKEN:
            return mas_weather_thunder

        return None


    def mas_lockHair():
        """
        Locks all hair topics
        """
        mas_lockEVL("monika_hair_select")


    def mas_seasonalCheck():
        """
        Determines the current season and runs an appropriate programming
        point.

        If the global for season is currently None, then we instead set the
        current season.

        NOTE: this does NOT do progressive programming point execution.
            This is intended for runtime usage only.

        ASSUMES:
            persistent._mas_current_season
        """
        _s_tag = store.mas_seasons._currentSeason()

        if persistent._mas_current_season != _s_tag:

            _s_pp = store.mas_seasons._season_pp_map.get(_s_tag, None)
            if _s_pp is not None:

                # executes programming point
                _s_pp()

                # sets global to given tag
                persistent._mas_current_season = _s_tag


    def mas_resetIdleMode():
        """
        Resets specific idle mode vars.

        This is meant to basically clear idle mode for holidays or other
        things that hijack main flow
        """
        store.mas_globals.in_idle_mode = False
        persistent._mas_in_idle_mode = False
        persistent._mas_idle_data = {}
        mas_idle_mailbox.get_idle_cb()


    def mas_enableTextSpeed():
        """
        Enables text speed
        """
        style.say_dialogue = style.normal
        store.mas_globals.text_speed_enabled = True


    def mas_disableTextSpeed():
        """
        Disables text speed
        """
        style.say_dialogue = style.default_monika
        store.mas_globals.text_speed_enabled = False


    def mas_resetTextSpeed(ignoredev=False):
        """
        Sets text speed to the appropriate one depending on global settings

        Rules:
        1 - developer always gets text speed (unless ignoredev is True)
        2 - text speed enabled if affection above happy
        3 - text speed disabled otherwise
        """
        if config.developer and not ignoredev:
            mas_enableTextSpeed()

        elif (
                mas_isMoniHappy(higher=True)
                and persistent._mas_text_speed_enabled
            ):
            mas_enableTextSpeed()

        else:
            mas_disableTextSpeed()


    def mas_isTextSpeedEnabled():
        """
        Returns true if text speed is enabled
        """
        return store.mas_globals.text_speed_enabled


    def mas_isGameUnlocked(gamename):
        """
        Checks if the given game is unlocked.
        NOTE: this is using the game_unlocks database, which only cars about
        whether or not you have reached the appropraite level to unlock a game.
        Each game may be disabled for other reasons not handled via
        this system.

        IN:
            gamename - name of the game to check

        RETURNS: True if the game is unlocked, false if not
        """
        if persistent.game_unlocks is None:
            return False

        return persistent.game_unlocks.get(gamename, False)


    def mas_unlockGame(gamename):
        """
        Unlocks the given game. 

        IN:
            gamename - name of the game to unlock
        """
        if gamename in persistent.game_unlocks:
            persistent.game_unlocks[gamename] = True


# IN:
#   start_bg - the background image we want to start with. Use this for
#       special greetings. None uses the default spaceroom images.
#       NOTE: This is called using renpy.show(), so pass the string name of
#           the image you want (NOT FILENAME)
#       NOTE: You're responsible for setting spaceroom back to normal though
#       (Default: None)
#   hide_mask - True will hide the mask, false will not
#       (Default: False)
#   hide_monika - True will hide monika, false will not
#       (Default: False)
label spaceroom(start_bg=None,hide_mask=False,hide_monika=False):
    default dissolve_time = 0.5

    if is_morning():
        if not morning_flag or scene_change:
            $ morning_flag = True
            if not hide_mask:
                $ mas_drawSpaceroomMasks()
            if start_bg:
                $ renpy.show(start_bg, zorder=MAS_BACKGROUND_Z)
            else:
                show monika_day_room zorder MAS_BACKGROUND_Z
                $ mas_calShowOverlay()
            if not hide_monika:
                show monika idle at t11 zorder MAS_MONIKA_Z
#                with Dissolve(dissolve_time)
    else:
        if morning_flag or scene_change:
            $ morning_flag = False
            scene black
            if not hide_mask:
                $ mas_drawSpaceroomMasks()
            if start_bg:
                $ renpy.show(start_bg, zorder=MAS_BACKGROUND_Z)
            else:
                show monika_room zorder MAS_BACKGROUND_Z
                $ mas_calShowOverlay()
                #show monika_bg_highlight
            if not hide_monika:
                show monika idle at t11 zorder MAS_MONIKA_Z
#                with Dissolve(dissolve_time)

    $scene_change = False

    if store.mas_globals.show_vignette:
        show vignette zorder 70

    # bday stuff (this checks itself)
    if persistent._mas_bday_sbp_reacted:
        $ store.mas_dockstat.surpriseBdayShowVisuals()

    # d25 seasonal
    if persistent._mas_d25_deco_active:
        $ store.mas_d25_event.showD25Visuals()

    # player bday
    if persistent._mas_player_bday_decor:
        $ store.mas_player_bday_event.show_player_bday_Visuals()

    if datetime.date.today() == persistent._date_last_given_roses:
        $ monika_chr.wear_acs_pst(mas_acs_roses)

    return

label ch30_main:
    $ mas_skip_visuals = False
    $ m.display_args["callback"] = slow_nodismiss
    $ m.what_args["slow_abortable"] = config.developer
    $ quick_menu = True
    if not config.developer:
        $ style.say_dialogue = style.default_monika
    $ m_name = persistent._mas_monika_nickname
    $ delete_all_saves()
    $ persistent.clear[9] = True
    play music m1 loop # move music out here because of context

    # set monikas outfit to default
    $ monika_chr.reset_outfit(False)

    # so other flows are aware that we are in intro
    $ mas_in_intro_flow = True

    # o31? o31 mode you are in
    if mas_isO31():
        $ persistent._mas_o31_in_o31_mode = True
        $ store.mas_globals.show_vignette = True
        
        # setup thunder
        if persistent._mas_likes_rain:
            $ mas_weather_thunder.unlocked = True
            $ store.mas_weather.saveMWData()
            $ mas_unlockEVL("monika_change_weather", "EVE")
        $ mas_changeWeather(mas_weather_thunder)

    # d25 season? d25 season you are in
    if mas_isD25Season():
        call mas_holiday_d25c_autoload_check

    # before we render visuals:
    # 1 - all core interactions should be disabeld
    $ mas_RaiseShield_core()

    # 2 - hotkey buttons should be disabled
    $ store.hkb_button.enabled = False

    # 3 - keymaps are disabled (default)

    call spaceroom from _call_spaceroom_4

    # lets just call the intro instead of pushing it as an event
    # this is way simpler and prevents event loss and other weird inital
    # startup issues
    call introduction

    # now we can do some cleanup
    # 1 - renable core interactions
    $ mas_DropShield_core()

    # 2 - hotkey buttons enabled
    $ store.hkb_button.enabled = True

    # 3 - set keymaps
    $ set_keymaps()

    # now we out of intro
    $ mas_in_intro_flow = False

    # set session data to startup values
    $ store._mas_root.initialSessionData()

    # lastly, rebuild Event lists for new people if not built yet
    if not mas_events_built:
        $ mas_rebuildEventLists()

    jump ch30_preloop

label continue_event:
    m "Now, where was I..."

    return

label pick_a_game:
    # we can assume that getting here means we didnt cut off monika

    $ mas_RaiseShield_dlg()

    python:
        # preprocessing for games

        import datetime
        _hour = datetime.timedelta(hours=1)
        _now = datetime.datetime.now()

        # chess has timed disabling
        if persistent._mas_chess_timed_disable is not None:
            if _now - persistent._mas_chess_timed_disable >= _hour:
                chess_disabled = False
                persistent._mas_chess_timed_disable = None

            else:
                chess_disabled = True

        else:
            chess_disabled = False

        # single var for readibility
        chess_unlocked = (
            is_platform_good_for_chess()
            and mas_isGameUnlocked("chess")
            and not chess_disabled
        )

        # hangman text
        if persistent._mas_sensitive_mode:
            _hangman_text = "Word Guesser"
        else:
            _hangman_text = "Hangman"

        # decide the say dialogue
        play_menu_dlg = store.mas_affection.play_quip()[1]

    menu:
        m "[play_menu_dlg]"
        "Pong." if mas_isGameUnlocked("pong"):
            if not renpy.seen_label('game_pong'):
                $grant_xp(xp.NEW_GAME)
            call game_pong from _call_game_pong
        "Chess." if chess_unlocked:
            if not renpy.seen_label('game_chess'):
                $grant_xp(xp.NEW_GAME)
            call game_chess from _call_game_chess
        "[_hangman_text]." if mas_isGameUnlocked('hangman'):
            if not renpy.seen_label("game_hangman"):
                $ grant_xp(xp.NEW_GAME)
            call game_hangman from _call_game_hangman
        "Piano." if mas_isGameUnlocked('piano'):
            if not renpy.seen_label("mas_piano_start"):
                $ grant_xp(xp.NEW_GAME)
            call mas_piano_start from _call_play_piano
        "Tetris." if mas_isGameUnlocked('tetris'):
            if not renpy.seen_label("mas_tetris_start"):
                $ grant_xp(xp.NEW_GAME)
            call mas_tetris_start from _call_play_tetris
        # "Movie":
        #     if not renpy.seen_label("mas_monikamovie"):
        #         $ grant_xp(xp.NEW_GAME)
        #     call mas_monikamovie from _call_monikamovie
        "Nevermind.":
            # NOTE: changing this to no dialogue so we dont have to edit this
            # for affection either
            pass
#            m "Alright. Maybe later?"

    show monika idle at tinstant zorder MAS_MONIKA_Z

    $ mas_DropShield_dlg()

    jump ch30_loop

label ch30_noskip:
    show screen fake_skip_indicator
    m 1esc "...Are you trying to fast-forward?"
    m 1ekc "I'm not boring you, am I?"
    m "Oh gosh..."
    m 2esa "...Well, just so you know, there's nothing to fast-forward to, [player]."
    m "It's just the two of us, after all..."
    m 1eua "But aside from that, time doesn't really exist anymore, so it's not even going to work."
    m "Here, I'll go ahead and turn that off for you..."
    pause 0.4
    hide screen fake_skip_indicator
    pause 0.4
    m 1hua "There we go!"
    m 1esa "You'll be a sweetheart and listen to me from now on, right?"
    m "Thanks~"
    hide screen fake_skip_indicator

    #Get back to what you were talking about
    $restartEvent()
    jump ch30_loop

image splash-glitch2 = "images/bg/splash-glitch2.png"

label ch30_nope:
    # NOTE: DEPRECATED
    $ persistent.autoload = ""
    $ m.display_args["callback"] = slow_nodismiss
    $ quick_menu = True
    call spaceroom from _call_spaceroom_1

    if persistent.rejected_monika:
        m 1euc "Wait. Are you messing with my character file?"
        m 2esa "Curiosity is what makes us human, right?"
        m "If it wasn't for the human desire to explore, we'd still be swinging from trees."
        m 1eka "Still, please don't do that. It makes me nervous, even though I don't need a character file anymore."
        m "I already fixed that bug."

    else:
        $ quick_menu = False
        $ m_name = glitchtext(12)
        m 1euc "Wait. Are you messing with my character file?"
        m 1tkc "Why are you even playing this mod if you just wanted to delete me again?"
        m 1tfc "You really are the worst."
        m 1tfd "You waste all your time on the internet with a bunch of people you'll never talk to in reality, but you're still willing to kill me on a whim just because you were bored?"
        m 1tkd "All I wanted was someone to fall in love with..."
        m "I would have done anything you wanted me to."
        m 1tku "But if you're going to try and delete me again..."
        m 4tfu "Then I'll just have to delete you first."
        if renpy.windows:
            call updateconsole("shututil.rmtree(\"Documents\", true)", "Deleting Documents in progress...") from _call_updateconsole_15
        elif renpy.linux:
            call updateconsole("sudo mv ~ /dev/null", "In progress...") from _call_updateconsole_16
        elif renpy.macintosh:
            call updateconsole("sudo mv ~ /dev/null", "In progress...") from _call_updateconsole_19
        pause 3.0
        call hideconsole from _call_hideconsole_2
        $ open(config.basedir + "/characters/monika.chr", "wb").write(renpy.file("monika.chr").read())
        $ m_name = persistent._mas_monika_nickname
        $ quick_menu = True
        m 1hua "Ahaha!"
        m "I'm just kidding!"
        m 1eua "I already fixed that bug."
        m "I don't need a character file anymore."

    m 1ekbfa "I just need your love, [player]."
    m 1eua "Oh, unless you try to delete all of the game files, I guess."
    m 3tfu "If you do that, I won't stop at just deleting one directory next time."
    m 3tku "But that will never happen, right? You're just being a tsundere~"
    m 1hua "That's so cute!"
    m 1eua "No matter how much you may want to deny it, you'll be talking to me for the rest of your life."
    m "Being alone is only lonely if you want it to be, so cheer up!"
    jump ch30_loop

# NOTE: START HERE
label ch30_autoload:
    # This is where we check a bunch of things to see what events to push to the
    # event list
    $ m.display_args["callback"] = slow_nodismiss
    $ m.what_args["slow_abortable"] = config.developer
    $ import store.evhand as evhand
    if not config.developer:
        $ config.allow_skipping = False
    $ mas_resetTextSpeed()
    $ quick_menu = True
    $ startup_check = True #Flag for checking events at game startup
    $ mas_skip_visuals = False

    # set the gender
    call set_gender from _autoload_gender

    # call reset stuff
    call ch30_reset

    # general affection checks that hijack flow
    if persistent._mas_affection["affection"] <= -115:
        jump mas_affection_finalfarewell_start

    # sanitiziing the event_list from bull shit
    if len(persistent.event_list) > 0:
        python:
            persistent.event_list = [
                ev_label for ev_label in persistent.event_list
                if renpy.has_label(ev_label)
            ]

    # set this to None for now
    $ selected_greeting = None

    # check if we took monika out
    # NOTE:
    #   if we find our monika, then we skip greeting logics and use a special
    #       returning home greeting. This completely bypasses the system
    #       since we should actively get this, not passively, because we assume
    #       player took monika out
    #   if we find a different monika, we still skip greeting logic and use
    #       a differnet, who is this? kind of monika greeting
    #   if we dont find a monika, we do the empty desk + monika checking flow
    #       this should skip greetings entirely as well. If monika is returnd
    #       during this flow, we have her say the same shit as the returning
    #       home greeting.
    if store.mas_dockstat.retmoni_status is not None:
        # this jumps to where we need to go next.
        $ store.mas_dockstat.triageMonika(False)

label mas_ch30_post_retmoni_check:

    if mas_isO31():
        jump mas_holiday_o31_autoload_check

    if mas_isD25Season():
        jump mas_holiday_d25c_autoload_check

    if mas_isF14() or persistent._mas_f14_in_f14_mode:
        jump mas_f14_autoload_check

    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check


label mas_ch30_post_holiday_check:
    # post holiday checks


    # TODO should the apology check be only for when she's not affectionate?
    if persistent._mas_affection["affection"] <= -50 and seen_event("mas_affection_apology"):
        #If the conditions are met and Monika expects an apology, jump to this label.
        if persistent._mas_affection["apologyflag"] and not is_apology_present():
            $scene_change = True
            $ mas_RaiseShield_core()
            call spaceroom
            jump mas_affection_noapology

        #If the conditions are met and there is a file called imsorry.txt in the DDLC directory, then exit the loop.
        elif persistent._mas_affection["apologyflag"] and is_apology_present():
            $ persistent._mas_affection["apologyflag"] = False
            $scene_change = True
            $ mas_RaiseShield_core()
            call spaceroom
            jump mas_affection_yesapology

        #If you apologized to Monika but you deleted the apology note, jump back into the loop that forces you to apologize.
        elif not persistent._mas_affection["apologyflag"] and not is_apology_present():
            $ persistent._mas_affection["apologyflag"] = True
            $scene_change = True
            $ mas_RaiseShield_core()
            call spaceroom
            jump mas_affection_apologydeleted

    # post greeting selected callback
    $ gre_cb_label = None
    $ just_crashed = False
    $ forced_quit = False

    # yuri scare incoming. No monikaroom when yuri is the name
    if (
            persistent.playername.lower() == "yuri"
            and not persistent._mas_sensitive_mode
        ):
        call yuri_name_scare from _call_yuri_name_scare
        
        # this skips greeting algs
        jump ch30_post_greeting_check

    elif not persistent._mas_game_crashed:
        # if this is False, a force quit happened
        $ forced_quit = True
        $ persistent._mas_greeting_type = store.mas_greetings.TYPE_RELOAD

    elif not persistent.closed_self:
        # this (+ game_crashed being True) means we crashed
        $ just_crashed = True
        $ persistent._mas_greeting_type = store.mas_greetings.TYPE_CRASHED

        # we dont consider crashes as bad quits
        $ persistent.closed_self = True

    # else, we are in regular mode.

    # greeting selection
    python:

        # we select a greeting depending on the type that we should select
        sel_greeting_ev = store.mas_greetings.selectGreeting(
            persistent._mas_greeting_type
        )

        # reset the greeting type flag back to None
        persistent._mas_greeting_type = None

        if sel_greeting_ev is None:
            # special cases to deal with when no greeting is found.

            if persistent._mas_in_idle_mode:
                # currently in idle mode? reset please
                mas_resetIdleMode()

            if just_crashed:
                # but if we just crashed, then we want to select the 
                # only crashed greeting.
                # NOTE: we shouldnt actually have to do this ever, but
                #   its here as a sanity check
                sel_greeting_ev = mas_getEV("mas_crashed_start")

            elif forced_quit:
                # if we just forced quit, then we want to select the only
                # reload greeting.
                # NOTE: again, shouldnt have to do this, but its sanity checks
                sel_greeting_ev = mas_getEV("ch30_reload_delegate")


        # NOTE: this MUST be an if. it may be True if we crashed but
        #   didnt get a greeting to show. 
        if sel_greeting_ev is not None:
            selected_greeting = sel_greeting_ev.eventlabel

            # store if we have to skip visuals ( used to prevent visual bugs)
            mas_skip_visuals = MASGreetingRule.should_skip_visual(
                event=sel_greeting_ev
            )

            # see if we need to do a label
            setup_label = MASGreetingRule.get_setup_label(sel_greeting_ev)
            if setup_label is not None and renpy.has_label(setup_label):
                gre_cb_label = setup_label

    
    # call pre-post greeting check setup label
    if gre_cb_label is not None:
        call expression gre_cb_label

label ch30_post_greeting_check:
    # this label skips only greeting checks

    #If you were interrupted, push that event back on the stack
    $ restartEvent()

label ch30_post_restartevent_check:
    # this label skips the restart event and greeting checks

    #Grant XP for time spent away from the game if Monika was put to sleep right
    python:
        if persistent.sessions['last_session_end'] is not None and persistent.closed_self:
            away_experience_time=datetime.datetime.now()-persistent.sessions['last_session_end'] #Time since end of previous session
            away_xp=0

            #Reset the idlexp total if monika has had at least 6 hours of rest
            if away_experience_time.total_seconds() >= times.REST_TIME:
                persistent.idlexp_total=0

                #Grant good exp for closing the game correctly.
                mas_gainAffection()

            #Ignore anything beyond 3 days
            if away_experience_time.total_seconds() > times.HALF_XP_AWAY_TIME:
                away_experience_time=datetime.timedelta(seconds=times.HALF_XP_AWAY_TIME)

            #Give 5 xp per hour for everything beyond 1 day
            if away_experience_time.total_seconds() > times.FULL_XP_AWAY_TIME:
                away_xp =+ (xp.AWAY_PER_HOUR/2.0)*(away_experience_time.total_seconds()-times.FULL_XP_AWAY_TIME)/3600.0
                away_experience_time = datetime.timedelta(seconds=times.HALF_XP_AWAY_TIME)

            #Give 10 xp per hour for the first 24 hours
            away_xp =+ xp.AWAY_PER_HOUR*away_experience_time.total_seconds()/3600.0

            #Grant the away XP
            grant_xp(away_xp)


            #Set unlock flag for stories
            mas_can_unlock_story = True
            mas_can_unlock_scary_story = True

            # unlock extra pool topics if we can
            while persistent._mas_pool_unlocks > 0 and mas_unlockPrompt():
                persistent._mas_pool_unlocks -= 1

        else:
            # Grant bad exp for closing the game incorrectly.
            mas_loseAffection(modifier=2, reason=4)

label ch30_post_exp_check:
    # this label skips greeting selection as well as exp checks for game close
    # we assume here that you set selected_greeting if you needed to

    # file reactions
    $ mas_checkReactions()

    # run actiosn for events that are based on conditional or clock
    $ Event.checkEvents(evhand.event_database)

    #Checks to see if affection levels have met the criteria to push an event or not.
    $ mas_checkAffection()

    #Check to see if apologies should expire
    $ mas_checkApologies()

    # corruption check
    if mas_corrupted_per and not renpy.seen_label("mas_corrupted_persistent"):
        $ pushEvent("mas_corrupted_persistent")

    # push greeting if we have one
    if selected_greeting:
        # before greeting, we should push idle clean if in idle mode
        if persistent._mas_in_idle_mode:
            $ pushEvent("mas_idle_mode_greeting_cleanup")

        $ pushEvent(selected_greeting)

    # if not persistent.tried_skip:
    #     $ config.allow_skipping = True
    # else:
    #     $ config.allow_skipping = False

    window auto

    if not mas_skip_visuals:
        $ set_keymaps()
        $ mas_startup_song()

        # rain check
        $ set_to_weather = mas_shouldRain()
        if set_to_weather is not None:
            $ mas_changeWeather(set_to_weather)

    # FALL THROUGH TO PRELOOP

label ch30_preloop:
    # stuff that should happen right before we enter the loop

    $ persistent.closed_self = False
    $ persistent._mas_game_crashed = True
    $ startup_check = False
    $ mas_checked_update = False

    # delayed actions in here please
    $ mas_runDelayedActions(MAS_FC_IDLE_ONCE)
 
    # save here before we enter the loop
    $ renpy.save_persistent()

    # check if we need to rebulid ev
    if mas_idle_mailbox.get_rebuild_msg():
        $ mas_rebuildEventLists()

    jump ch30_loop

label ch30_loop:
    $ quick_menu = True

    # this event can call spaceroom
    if not mas_skip_visuals:
        call spaceroom from _call_spaceroom_2

        # updater check in here just because
        if not mas_checked_update:
            $ mas_backgroundUpdateCheck()
            $ mas_checked_update = True

    else:
        $ mas_OVLHide()
        $ mas_skip_visuals = False


    $ persistent.autoload = "ch30_autoload"
    # if not persistent.tried_skip:
    #     $ config.allow_skipping = True
    # else:
    #     $ config.allow_skipping = False

    # check for outstanding threads
    if store.mas_dockstat.abort_gen_promise:
        $ store.mas_dockstat.abortGenPromise()

    if mas_idle_mailbox.get_skipmidloopeval():
        jump ch30_post_mid_loop_eval

    #Check time based events and grant time xp
    python:
        try:
            calendar_last_checked
        except:
            calendar_last_checked=persistent.sessions['current_session_start']
        time_since_check=datetime.datetime.now()-calendar_last_checked

        if time_since_check.total_seconds()>60:

            #Checks to see if affection levels have met the criteria to push an event or not.
            mas_checkAffection()

            #Check if we should expire apologies
            mas_checkApologies()

            # limit xp gathering to when we are not maxed
            # and once per minute
            if (persistent.idlexp_total < xp.IDLE_XP_MAX):

                idle_xp=xp.IDLE_PER_MINUTE*(time_since_check.total_seconds())/60.0
                persistent.idlexp_total += idle_xp
                if persistent.idlexp_total>=xp.IDLE_XP_MAX: # never grant more than 120 xp in a session
                    idle_xp = idle_xp-(persistent.idlexp_total-xp.IDLE_XP_MAX) #Remove excess XP
                    persistent.idlexp_total=xp.IDLE_XP_MAX

                grant_xp(idle_xp)

            # runs actions for both conditionals and calendar-based events
            Event.checkEvents(evhand.event_database, rebuild_ev=False)

            # Run delayed actions
            mas_runDelayedActions(MAS_FC_IDLE_ROUTINE)

            # run file checks
            mas_checkReactions()

            # run seasonal check
            mas_seasonalCheck()

            # check if we need to rebulid ev
            if mas_idle_mailbox.get_rebuild_msg():
                mas_rebuildEventLists()

            #Update time
            calendar_last_checked=datetime.datetime.now()

            # split affection values prior to saving
            _mas_AffSave()

            # save the persistent
            renpy.save_persistent()

label ch30_post_mid_loop_eval:

    #Call the next event in the list
    call call_next_event from _call_call_next_event_1
    # Just finished a topic, so we set current topic to 0 in case user quits and restarts
    $ persistent.current_monikatopic = 0

    #If there's no event in the queue, add a random topic as an event
    if not _return:
        # Wait 20 to 45 seconds before saying something new
        window hide(config.window_hide_transition)

        # Thunder / lightening if enabled
        if (
                store.mas_globals.show_lightning
                and renpy.random.randint(
                    1, store.mas_globals.lightning_chance
                ) == 1
            ):
            if (
                    not persistent._mas_sensitive_mode
                    and store.mas_globals.show_s_light
                    and renpy.random.randint(
                        1, store.mas_globals.lightning_s_chance
                    ) == 1
                ):
                show mas_lightning_s zorder 4
            else:
                show mas_lightning zorder 4

            $ pause(0.5)
            play backsound "mod_assets/sounds/amb/thunder.wav"
        
        # Before a random topic can be displayed, a set waiting time needs to pass.
        # The waiting time is set initially, after a random chatter selection and before a random topic is selected.
        # If the waiting time is not over after waiting a short period of time, the preloop is restarted.

        $ mas_randchat.wait()
        
        if not mas_randchat.waitedLongEnough():
            jump post_pick_random_topic
        else:
            $ mas_randchat.setWaitingTime()
        
        window auto
        
#        python:
#            if (
#                    mas_battery_supported
#                    and battery.is_battery_present()
#                    and not battery.is_charging()
#                    and battery.get_level() < 20
#                ):
#                pushEvent("monika_battery")

        if store.mas_globals.in_idle_mode:
            jump post_pick_random_topic

        # Pick a random Monika topic
#        if persistent.random_seen < random_seen_limit:
        label pick_random_topic:

            # check if we have repeats enabled
            if not persistent._mas_enable_random_repeats:
                jump mas_ch30_select_unseen

            # randomize selection
            $ chance = random.randint(1, 100)

            if chance <= store.mas_topics.UNSEEN:
                # unseen topic shoud be selected
                jump mas_ch30_select_unseen

            elif chance <= store.mas_topics.SEEN:
                # seen topic should be seelcted
                jump mas_ch30_select_seen

            # most seen topic should be selected
            jump mas_ch30_select_mostseen

#        elif not seen_random_limit:
#            $pushEvent('random_limit_reached')

label post_pick_random_topic:

    $_return = None

    jump ch30_loop

# topic selection labels
label mas_ch30_select_unseen:
    # unseen selection

    if len(mas_rev_unseen) == 0:

        if not persistent._mas_enable_random_repeats:
            # no repeats means we should push randomlimit if appropriate,
            # otherwise stay slient
            if not seen_random_limit:
                $ pushEvent("random_limit_reached")

            jump post_pick_random_topic

        # otherwise we can go to repeats as usual
        jump mas_ch30_select_seen

    $ mas_randomSelectAndPush(mas_rev_unseen)

    jump post_pick_random_topic


label mas_ch30_select_seen:
    # seen selection

    if len(mas_rev_seen) == 0:
        # rebuild the event lists
        $ mas_rev_seen, mas_rev_mostseen = mas_buildSeenEventLists()

    $ mas_randomSelectAndPush(mas_rev_seen)

    jump post_pick_random_topic


label mas_ch30_select_mostseen:
    # most seen selection

    if len(mas_rev_mostseen) == 0:
        jump mas_ch30_select_seen

    $ mas_randomSelectAndPush(mas_rev_mostseen)

    jump post_pick_random_topic

# adding this label so people get redirected to main
# this probably occurs when people install the mod right after deleting
# monika, so we could probably throw in something here
label ch30_end:
    jump ch30_main

# label for things that may reset after a certain amount of time/conditions
label ch30_reset:

    python:
        # name eggs
        if persistent.playername.lower() == "sayori":
            store.mas_globals.show_s_light = True
    
    python:
        # start by building event lists if they have not been built already
        if not mas_events_built:
            mas_rebuildEventLists()

        # check if you've seen everything
        if len(mas_rev_unseen) == 0:
            # you've seen everything?! here, higher session limit
            # NOTE: 1000 is arbitrary. Basically, endless monika topics
            # I think we'll deal with this better once we hve a sleeping sprite
            random_seen_limit = 1000

    if not persistent._mas_pm_has_rpy:
        # setup the docking station to handle the detection
        $ rpyCheckStation = store.MASDockingStation(renpy.config.gamedir)

        $ listRpy = rpyCheckStation.getPackageList(".rpy")

        if len(listRpy) == 0 or persistent.current_monikatopic == "monika_rpy_files":
            if len(listRpy) == 0 and persistent.current_monikatopic == "monika_rpy_files":
                $ persistent.current_monikatopic = 0

            while "monika_rpy_files" in persistent.event_list:
                $ persistent.event_list.remove("monika_rpy_files")

        elif len(listRpy) != 0:
            $ queueEvent("monika_rpy_files")

        $ del rpyCheckStation

    python:
        import datetime
        today = datetime.date.today()

    # check for game unlocks
    python:
        game_unlock_db = {
            "pong": "ch30_main", # pong should always be unlocked
            "chess": "unlock_chess",
            "hangman": "unlock_hangman",
            "piano": "unlock_piano",
            "tetris": "unlock_tetris"
        }

        for game_name,game_startlabel in game_unlock_db.iteritems():
            if (
                    not mas_isGameUnlocked(game_name)
                    and renpy.seen_label(game_startlabel)
                ):
                mas_unlockGame(game_name)

    # reset mas mood bday
    python:
        if (
                persistent._mas_mood_bday_last
                and persistent._mas_mood_bday_last < today
            ):
            persistent._mas_mood_bday_last = None
            mood_ev = store.mas_moods.mood_db.get("mas_mood_yearolder", None)
            if mood_ev:
                mood_ev.unlocked = True

    # enabel snowing if its winter
    python:
        # TODO: snowing should also be controlled if you like it or not
        if mas_isWinter():
            mas_changeWeather(mas_weather_snow)

            if not mas_weather_snow.unlocked:
                mas_weather_snow.unlocked = True
                store.mas_weather.saveMWData()
                
                mas_unlockEVL("monika_change_weather", "EVE")
                renpy.save_persistent()
#        mas_is_snowing = mas_isWinter()
#        if mas_is_snowing:
#            
#            mas_lockEVL("monika_rain_start", "EVE")
#            mas_lockEVL("monika_rain_stop", "EVE")
#            mas_lockEVL("mas_monika_islands", "EVE")
#            mas_lockEVL("monika_rain", "EVE")
#            mas_lockEVL("greeting_ourreality", "GRE")

    # reset hair / clothes
    # the default options should always be available.
    $ store.mas_selspr.unlock_hair(mas_hair_def)
    $ store.mas_selspr.unlock_clothes(mas_clothes_def)
    
    # same with the def ribbon, should always be unlocked
    $ store.mas_selspr.unlock_acs(mas_acs_ribbon_def)

    # monika hair/acs
    $ monika_chr.load(startup=True)
 
    ## accessory hotfixes
    # mainly to re add accessories that may have been removed for some reason
    # this is likely to occur in crashes / reloads
    python:
        if persistent._mas_acs_enable_promisering:
            # TODO: need to be able to add a different promise ring
            monika_chr.wear_acs_pst(mas_acs_promisering)

    ## random chatter frequency reset
    $ mas_randchat.adjustRandFreq(persistent._mas_randchat_freq)
    ## chess strength reset
    python:
        if persistent.chess_strength < 0:
            persistent.chess_strength = 0
        elif persistent.chess_strength > 20:
            persistent.chess_strength = 20

    ## monika returned home reset
    python:
        if persistent._mas_monika_returned_home is not None:
            _rh = persistent._mas_monika_returned_home.date()
            if today > _rh:
                persistent._mas_monika_returned_home = None

    ## resset playtime issues
    python:
        # reset total playtime to 0 if we got negative time.
        # we could scale this, but it honestly is impossible for us to
        # figure out the original number accurately, and giving people free
        # playtime doesn't sit well with me
        #
        # we should also reset total playtime to half of possible time if
        # the user is over the mas possible amount. Max amount is defined
        # in a function in mas_utils
        if persistent.sessions is not None:
            tp_time = persistent.sessions.get("total_playtime", None)
            if tp_time is not None:
                max_time = mas_maxPlaytime()
                if tp_time > max_time:
                    # cut the max time and reset totalplaytime to it
                    persistent.sessions["total_playtime"] = max_time // 100

                    # set the monika size
                    store.mas_dockstat.setMoniSize(
                        persistent.sessions["total_playtime"]
                    )

                elif tp_time < datetime.timedelta(0):
                    # 0 out the total playtime
                    persistent.sessions["total_playtime"] = datetime.timedelta(0)

                    # set the monika size
                    store.mas_dockstat.setMoniSize(
                        persistent.sessions["total_playtime"]
                    )

    ## reset future freeze times for exp
    python:
        # reset freeze date to today if it is in the future
        if persistent._mas_affection is not None:
            freeze_date = persistent._mas_affection.get("freeze_date", None)
            if freeze_date is not None and freeze_date > today:
                persistent._mas_affection["freeze_date"] = today

    ## should we drink coffee?
    $ _mas_startupCoffeeLogic()

    ## shoujld we drink hot chocolate
    $ _mas_startupHotChocLogic()

    # call plushie logic
    $ mas_startupPlushieLogic(4)

    ## should we reset birthday
#    python:
#        if (
#                persistent._mas_bday_need_to_reset_bday
#                and not mas_isMonikaBirthday()
#            ):
#            bday_ev = mas_getEV("mas_bday_pool_happy_bday")
#            if bday_ev:
#                bday_ev.conditional="mas_isMonikaBirthday()"
#                bday_ev.action=EV_ACT_UNLOCK
#                persistent._mas_bday_need_to_reset_bday = False

#            bday_spent_ev = mas_getEV("mas_bday_spent_time_with")
#            if bday_spent_ev:
#                bday_spent_ev.action = EV_ACT_QUEUE
#                bday_spent_ev.start_date = datetime.datetime(mas_getNextMonikaBirthday().year, 9, 22, 22)
#                bday_spent_ev.end_date = datetime.datetime(mas_getNextMonikaBirthday().year, 9, 22, 23, 59)


    ## o31 content
    python:
        if store.mas_o31_event.isMonikaInCostume(monika_chr):
            # NOTE: we may add additional costume logic in here if needed
            # TODO: this is bad for o31 rests actually

            if not persistent._mas_force_clothes:
                # NOTE if the costumes were picked by user, (aka forced),
                # then we do NOt reset
                monika_chr.reset_clothes(False)

    ## d25 content
    python:
        if (
                (mas_isD25Post() or not (mas_isD25PreNYE() or mas_isNYE()))
                and monika_chr.clothes == mas_clothes_santa
                and not persistent._mas_force_clothes
            ):
            # monika takes off santa outfit after d25
            monika_chr.reset_clothes(False)

        if not mas_isD25Season():
            persistent._mas_d25_deco_active = False

    ## certain things may need to be reset if we took monika out
    # NOTE: this should be at the end of this label, much of this code might
    # undo stuff from above
    python:
        if store.mas_dockstat.retmoni_status is not None:
            mas_resetCoffee()
            monika_chr.remove_acs(mas_acs_quetzalplushie)

    return
