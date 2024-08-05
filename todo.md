- DONE Figure out character input
  - getch for an charcode
  - getkey for a string
- DONE Move the grid based on character input
- DONE Detect resize
  - getkey == 'KEY_RESIZE'
- DONE Colors
- DONE Draw a Grid
- Figure out standard Views
  - DONE AccordionView
  - DONE BarIndicator (Progress Indicator, Volume Display, etc.
  - DONE Box
  -      Browser
  -      Button (Styles Normal, Radio, CheckBox)
  -      ColorPicker (Swatch w/ RGB values you can edit w/ arrows and digit inputs)
  -      ComboBox
  -      DatePicker
  - DONE Image
  - DONE ImageView
  - DONE ListView (nested lists with expansion)
  -      Menu (manages how panels w/ menuviews are opened in response to selections)
  -      MenuView
  -      Panels (Generic/Open/Save)
  -      PopUpButton (Same as a menu item?))
  - DONE ScrollView
  -      SearchField
  - DONE SplitView
  - DONE Slider
  -      Stepper
  - DONE TabView
  - DONE TextView
  -      TextField
  - DONE TextFoldView

navigation ideas:

- unmodified keys are view-defined behavior
- Ctrl modified keys are for navigation between the controls in the application

# class hierarchy

-      Color
-      Event
-      Image
- ████ Menu
-      Point
-      Responder
  -      Application
  - ████ Panel
    - Make sure that views and responder chains know about panels
      - View::panel or Responder::panel
      - Responder::next_responder
  -      View
    -      (Control)
    -      AccordionView
    -      BarIndicator
    -      Box
    - ████ Browser
    -      Button
    -      ClipView
    - ████ ColorPicker
    -      ColorSwatch
    - ████ ComboBox / PopUpButton
    - ████ DatePicker
    -      EmptyView
    -      FillView
    -      ImageView
    -      ListView
    - ████ MenuView
    -      Scroller
    -      ScrollView
    - ████ SearchField
    -      Slider
    -      SplitView
    -      Stepper
    -      TabView
    -      TextField
    -      TextFoldView
    -      TextView
-      Screen
-      Size
-      Tixel