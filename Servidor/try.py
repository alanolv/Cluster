import moviepy.editor as mp 
import cv2



#corta el video en clipas para los slaves
def cliping(video_location, num_clips):
    # Load the video clip
    clip = mp.VideoFileClip(video_location)
    cap = cv2.VideoCapture('dukibn.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)
    


    total_duration = clip.duration  # Duración total del video en segundos
    print ("duracion",total_duration)

    duration_per_clip = total_duration / num_clips  # Duración por cada clip
    print ("\nduration_per_clip ",duration_per_clip)
    
    clips = []  # Almacena los nombres de los clips generados
    
    # Dividir el video en el número de clips especificado
    for i in range(num_clips):

        start_time = i * duration_per_clip
        print ("start_time ",start_time)

        end_time = start_time + duration_per_clip
        print ("end_time ",end_time)

        print ("fps ",fps)
        
        # Nombre del clip basado en su número de orden
        clip_name = f"clip_{i + 1}.mp4"
        
        # Llamar a la función cut_video() para cortar cada sección del video
        cut_video(video_location, start_time, end_time, clip_name,fps)
        
        clips.append(clip_name)  # Agregar el nombre del clip a la lista de clips generados
    
    return clips


def cut_video(videoLocation, start_time, end_time, clipName, fps):

    # Load the video clip
    clip = mp.VideoFileClip(videoLocation)
    
    
    # Create a cropped subclip  
    cropped_clip = clip.subclip(start_time, end_time)

    # Create VideoWriter object to save the modified frames
    cropped_clip.write_videofile(clipName, codec='libx264', fps=cropped_clip.fps)
    

    return clipName


#cliping(video_location="dukibn.mp4", num_clips = 2)

cliping(video_location="dukibn.mp4", num_clips = 4)